import logging
import os
import random
import sys
from logging.handlers import RotatingFileHandler

import psycopg
from telegram import Chat, ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode, UpdateType
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

logging.basicConfig(
    level=logging.WARNING,
    filename='main_log.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
handler = RotatingFileHandler('bot_log.log', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)

MAX_SET: dict = {
    'Ч': 287864,
    'Б': 37367,
    'Я': 5642
}
CORRESPONDANCE: dict = {
    'Что-Где-Когда': 'Ч',
    'Брейн-ринг': 'Б',
    'Своя игра': 'Я',
}
ANSWER_TEXT: None | str = None
CURRENT_QUESTION_TYPE: None | str = 'Ч'


def check_tokens(token) -> bool:
    """Проверяет доступность переменных окружения."""
    return bool(token)


def button_shortcut(button_names: list[list]) -> ReplyKeyboardMarkup:
    """Формирует кнопку с указанными полями."""
    return ReplyKeyboardMarkup(
        keyboard=button_names,
        resize_keyboard=True
    )


async def send_message(
        context: ContextTypes.DEFAULT_TYPE,
        chat: Chat,
        text: str,
        buttons: ReplyKeyboardMarkup,
        parse_mode=None) -> None:
    """Отправляет сообщение с указанными текстом и кнопками."""
    await context.bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=buttons,
        disable_web_page_preview=True,
        parse_mode=parse_mode
    )


async def get_question(question_type: str) -> None | dict:
    """Генерирует случайный вопрос и форматирует его."""
    try:
        async with await psycopg.AsyncConnection.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            # закомментировать при подключении к локальной БД
            host=os.getenv('DB_HOST'),
        ) as aconn:
            start_point = random.randint(0, MAX_SET[question_type] - 1)
            async with aconn.cursor() as acur:
                await acur.execute(
                    """SELECT question,
                            answer,
                            pass_criteria,
                            comments,
                            authors,
                            sources
                        FROM questions_question
                        WHERE (NOT is_condemned AND question_type = (%s))
                        LIMIT 1
                        OFFSET (%s);""",
                    (question_type, start_point)
                )
                question = await acur.fetchone()
    except Exception as error:
        logging.error(error, exc_info=True)
        return None
    if not question:
        logging.error(
            'Из бд был получен вопрос, интерпретируемый как None',
            exc_info=True
        )
        return None
    if question[0] == 'None' or question[1] == 'None':
        return None
    parsed_question = {'Вопрос': question[0], 'Ответ': question[1]}
    if question[2] != 'None':
        parsed_question['Зачёт'] = question[2]
    if question[3] != 'None':
        parsed_question['Комментарий'] = question[3]
    if question[4] != 'None':
        parsed_question['Авторы'] = question[4]
    if question[5] != 'None':
        parsed_question['Источники'] = question[5]
    return parsed_question


def generate_answer(parsed_question: dict) -> str:
    """Возвращает форматированную строку ответа на вопрос."""
    answer_dict = parsed_question.copy()
    del answer_dict['Вопрос']
    ANSWER_TEXT = f'<b>{answer_dict['Ответ']}</b>\n\n'
    del answer_dict['Ответ']
    ANSWER_TEXT += '\n'.join(f'<b><i>{key}:</i></b> <i>{item}</i>'
                             for key, item in answer_dict.items())
    return ANSWER_TEXT


async def handle_bd_error(context: ContextTypes.DEFAULT_TYPE,
                          chat: Chat) -> None:
    """Генерирует сообщение об ошибке запроса к API."""
    buttons = button_shortcut([['На главную'],])
    text = ('Произошла ошибка при выполнении запроса к базе данных 😳\n'
            'Попробуйте повторить попытку позже')
    await send_message(context, chat, text, buttons)


async def wake_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Генерирует начальное приветствие."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = button_shortcut([
        ['Что-Где-Когда'], ['Брейн-ринг'], ['Своя игра'], ['На главную'],
    ],)
    text = f'Здравствуйте, {name}! Выберите тип вопроса:'
    await send_message(context, chat, text, buttons)


async def handle_messages(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений от пользователя."""
    global ANSWER_TEXT, CURRENT_QUESTION_TYPE
    chat = update.effective_chat
    message = update.message.text
    if message in ('Что-Где-Когда', 'Брейн-ринг',
                   'Своя игра', 'Следующий вопрос'):
        if message == 'Следующий вопрос' and not CURRENT_QUESTION_TYPE:
            buttons = button_shortcut([['На главную'],])
            text = 'Если не было первого вопроса - не будет и следующего'
            await send_message(context, chat, text, buttons)
        else:
            parsed_question = (
                await get_question(CURRENT_QUESTION_TYPE)
                if CURRENT_QUESTION_TYPE
                else await get_question(CORRESPONDANCE[message])
            )
            if not parsed_question:
                await handle_bd_error(context, chat)
            else:
                if message != 'Следующий вопрос':
                    CURRENT_QUESTION_TYPE = CORRESPONDANCE[message]
                ANSWER_TEXT = generate_answer(parsed_question)
                buttons = button_shortcut([['Узнать ответ'], ['На главную'],])
                question = parsed_question['Вопрос']
                text = f'<i>Внимание, вопрос!</i>\n\n{question}'
                await send_message(context, chat, text,
                                   buttons, parse_mode=ParseMode.HTML)
    elif message == 'Узнать ответ':
        buttons = button_shortcut([['Следующий вопрос'], ['На главную'],])
        if ANSWER_TEXT:
            await send_message(context, chat, ANSWER_TEXT,
                               buttons, parse_mode=ParseMode.HTML)
            ANSWER_TEXT = None
        else:
            buttons = button_shortcut([['На главную'],])
            text = 'Сперва получите вопрос, на который хотите узнать ответ'
            await send_message(context, chat, text, buttons)
    elif message == 'На главную':
        CURRENT_QUESTION_TYPE = None
        ANSWER_TEXT = None
        await wake_up(update, context)
    else:
        buttons = button_shortcut([['На главную'],])
        text = ('Введите что-нибудь осмысленное, '
                'а лучше воспользуйтесь кнопками')
        await send_message(context, chat, text, buttons)


def main() -> None:
    """Start the bot."""
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    if not check_tokens(TELEGRAM_TOKEN):
        error_message = ('Работа бота остановлена:'
                         ' ошибка получения переменных окружения')
        logging.critical(error_message, exc_info=True)
        sys.exit(error_message)
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", wake_up))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_messages
    ))
    application.run_polling(allowed_updates=UpdateType.MESSAGE)


if __name__ == "__main__":
    main()
