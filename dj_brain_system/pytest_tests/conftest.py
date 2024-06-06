import pytest

from brain_system.models import (BoughtInProduct, BoughtInProductAsAPartOf,
                                 BoughtInProductLink)
from questions.models import Questions


@pytest.fixture
def bought_in_product_as_a_part_of():
    """
    Создает одну запись в таблице "BoughtInProductAsAPartOf".
    """
    return BoughtInProductAsAPartOf.objects.create(
        name='Блок_1',
    )


@pytest.fixture
def bought_in_product(bought_in_product_as_a_part_of):
    """
    Создает одну запись в таблице "BoughtInProduct".
    """
    return BoughtInProduct.objects.create(
        name='Деталь_1',
        a_part_of=bought_in_product_as_a_part_of,
        quantity=1,
        product_type='Тип_1',
        comment='Комментарий_1',
    )


@pytest.fixture
def bought_in_product_link(bought_in_product):
    """
    Создает две записи в таблице "BoughtInProductLink",
    связанные с одним объектом BoughtInProduct.
    """
    return BoughtInProductLink.objects.bulk_create([
        BoughtInProductLink(
            product=bought_in_product,
            link='https://example1.com',
            link_short_name='example1'
        ),
        BoughtInProductLink(
            product=bought_in_product,
            link='https://example2.com',
            link_short_name='example2'
        ),
    ])


@pytest.fixture
def feedback_form_data():
    """
    Возвращает словарь с данными для ввода в форму фидбэка.
    """
    return {
        'name': 'Автор фидбека',
        'email': 'someuser@example.com',
        'feedback_text': 'Текст фидбека',
        'captcha_0': 'dummy-value',
        'captcha_1': 'PASSED',
    }


@pytest.fixture
def question_add_form_data():
    """
    Возвращает словарь с данными для ввода в форму
    добавления нового вопроса в БД.
    """
    return {
        'question_type': 'Ч',
        'question': 'Текст вопроса',
        'answer': 'Ответ на вопрос',
    }


@pytest.fixture
def question_set():
    """
    Создает двадцать записей в таблице "Questions".
    """
    questions = []
    for i in range(1, 21):
        questions.append(
            Questions(
                package='Пакет',
                tour='Тур',
                number=i,
                question_type='Ч',
                question=f'Текст вопроса {i}',
                answer=f'Ответ на вопрос {i}',
                pass_criteria=f'Критерий для вопроса {i}',
                authors=f'Авторы вопроса {i}',
                sources=f'Источники вопроса {i}',
                comments=f'Комментарий к вопросу {i}',
                is_published=True,
            )
        )
    return Questions.objects.bulk_create(questions)


@pytest.fixture
def question_form_data():
    """
    Возвращает словарь с данными для ввода в форму
    для генерации случайных вопросов.
    """
    return {
        'question_type': 'Ч',
        'search_pattern': '',
        'questions_quantity': '10',
        'questions_displayed_on_page': '5',
    }
