import logging
import os
import random
import sys
from logging.handlers import RotatingFileHandler
from typing import Union

import psycopg2
# Раскомментировать при запуске не в составе docker compose
# from dotenv import load_dotenv
from telegram import Chat, ParseMode, ReplyKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

logging.basicConfig(
    level=logging.WARNING,
    filename='main_log.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
handler = RotatingFileHandler('bot_log.log', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)

CORRESPONDANCE: dict = {
    'Что-Где-Когда': 'Ч',
    'Брейн-ринг': 'Б',
    'Своя игра': 'Я',
}
ANSWER_TEXT: Union[None, str] = None
CURRENT_QUESTION_TYPE: Union[None, str] = 'Ч'

MAX_SET: dict = {
    'Ч': 287864,
    'Б': 37367,
    'Я': 5642
}

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
DB_PATH: str = os.path.join(BASE_DIR, 'db_main.sqlite')


def get_question(question_type: str) -> Union[None, dict]:
    """Генерирует случайный вопрос и форматирует его."""
    try:
        with psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB_NAME'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('DB_HOST'),
        ) as conn:
            start_point = random.randint(0, MAX_SET[question_type] - 1)
            curs = conn.cursor()
            curs.execute(
                """SELECT question,
                          answer,
                          pass_criteria,
                          comments,
                          authors,
                          sources
                    FROM questions_questions
                    WHERE (NOT condemned AND question_type = (%s))
                    LIMIT 1
                    OFFSET (%s);""",
                (question_type, start_point)
            )
            question = curs.fetchone()
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


def check_tokens() -> bool:
    """Проверяет доступность переменных окружения."""
    return bool(TELEGRAM_TOKEN)


def wake_up(update: Update, context: CallbackContext) -> None:
    """Генерирует начальное приветствие."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = button_shortcut([
        ['Что-Где-Когда'], ['Брейн-ринг'], ['Своя игра'], ['На главную'],
    ],)
    text = f'Здравствуйте, {name}! Выберите тип вопроса:'
    send_message(context, chat, text, buttons)


def handle_bd_error(context: CallbackContext, chat: Chat) -> None:
    """Генерирует сообщение об ошибке запроса к API."""
    buttons = button_shortcut([['На главную'],])
    text = ('Произошла ошибка при выполнении запроса к базе данных 😳\n'
            'Попробуйте повторить попытку позже')
    send_message(context, chat, text, buttons)


def button_shortcut(button_names: list[list]) -> ReplyKeyboardMarkup:
    """
    Формирует кнопку с указанными полями.
    """
    return ReplyKeyboardMarkup(
        keyboard=button_names,
        resize_keyboard=True
    )


def generate_answer(parsed_question: dict) -> str:
    """
    Возвращает форматированную строку ответа на вопрос.
    """
    answer_dict = parsed_question.copy()
    del answer_dict['Вопрос']
    answer = answer_dict['Ответ']
    ANSWER_TEXT = f'<b>{answer}</b>\n\n'
    del answer_dict['Ответ']
    ANSWER_TEXT += '\n'.join(f'<b><i>{key}:</i></b> <i>{item}</i>'
                             for key, item in answer_dict.items())
    return ANSWER_TEXT


def send_message(context: CallbackContext,
                 chat: Chat,
                 text: str,
                 buttons: ReplyKeyboardMarkup,
                 parse_mode=None) -> None:
    """
    Отправляет сообщение с указанными текстом и кнопками.
    """
    return context.bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=buttons,
        disable_web_page_preview=True,
        parse_mode=parse_mode
    )


def handle_messages(update: Update, context: CallbackContext) -> None:
    """
    Обработчик текстовых сообщений от пользователя.
    """
    global ANSWER_TEXT, CURRENT_QUESTION_TYPE
    chat = update.effective_chat
    message = update.message.text
    if message in ('Что-Где-Когда', 'Брейн-ринг',
                   'Своя игра', 'Следующий вопрос'):
        if message == 'Следующий вопрос' and not CURRENT_QUESTION_TYPE:
            buttons = button_shortcut([['На главную'],])
            text = 'Если не было первого вопроса - не будет и следующего'
            send_message(context, chat, text, buttons)
        else:
            parsed_question = (
                get_question(CURRENT_QUESTION_TYPE)
                if CURRENT_QUESTION_TYPE
                else get_question(CORRESPONDANCE[message])
            )
            if not parsed_question:
                handle_bd_error(context, chat)
            else:
                if message != 'Следующий вопрос':
                    CURRENT_QUESTION_TYPE = CORRESPONDANCE[message]
                ANSWER_TEXT = generate_answer(parsed_question)
                buttons = button_shortcut([['Узнать ответ'], ['На главную'],])
                question = parsed_question['Вопрос']
                text = f'<i>Внимание, вопрос!</i>\n\n{question}'
                send_message(context, chat, text,
                             buttons, parse_mode=ParseMode.HTML)
    elif message == 'Узнать ответ':
        buttons = button_shortcut([['Следующий вопрос'], ['На главную'],])
        if ANSWER_TEXT:
            send_message(context, chat, ANSWER_TEXT,
                         buttons, parse_mode=ParseMode.HTML)
            ANSWER_TEXT = None
        else:
            buttons = button_shortcut([['На главную'],])
            text = 'Сперва получите вопрос, на который хотите узнать ответ'
            send_message(context, chat, text, buttons)
    elif message == 'На главную':
        CURRENT_QUESTION_TYPE = None
        ANSWER_TEXT = None
        wake_up(update, context)
    else:
        buttons = button_shortcut([['На главную'],])
        text = ('Введите что-нибудь осмысленное, '
                'а лучше воспользуйтесь кнопками')
        send_message(context, chat, text, buttons)


if __name__ == '__main__':
    # Раскомментировать при запуске не в составе docker compose
    # load_dotenv()
    TELEGRAM_TOKEN: str = os.getenv('TEST_TELEGRAM_TOKEN')
    if not check_tokens():
        error_message = ('Работа бота остановлена:'
                         ' ошибка получения переменных окружения')
        logging.critical(error_message)
        sys.exit(error_message)
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(
        CommandHandler(('start',), wake_up)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, handle_messages)
    )
    updater.start_polling()
    updater.idle()
