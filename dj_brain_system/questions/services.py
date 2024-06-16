import datetime
import random

from django.core.paginator import Paginator

from .models import Question

MAX_SET_JEOPARDY = None
MAX_SET_BRAIN = None
MAX_SET_WWW = None
LAST_REFRESH = datetime.datetime.now()
REFRESH_INTERVAL = datetime.timedelta(hours=8)
SET_FOR_RANDOMIZING: int = 5000


def get_max_question_sets():
    """Пересчитывает количество вопросов в БД по трем категориям через
    заданный в параметре REFRESH_INTERVAL интервал времени."""
    global MAX_SET_WWW, MAX_SET_BRAIN, MAX_SET_JEOPARDY, LAST_REFRESH
    if (
        not all([MAX_SET_JEOPARDY, MAX_SET_BRAIN, MAX_SET_WWW,])
        or (datetime.datetime.now() - LAST_REFRESH > REFRESH_INTERVAL)
    ):
        MAX_SET_WWW = Question.objects.filter(question_type='Ч').count()
        MAX_SET_BRAIN = Question.objects.filter(question_type='Б').count()
        MAX_SET_JEOPARDY = Question.objects.filter(question_type='Я').count()
        LAST_REFRESH = datetime.datetime.now()
    return {
        'Ч': MAX_SET_WWW,
        'Б': MAX_SET_BRAIN,
        'Я': MAX_SET_JEOPARDY
    }


def get_initial_queryset(question_type):
    """Формирует первоначальный список вопросов с учетом типа вопроса и
    заданного константой "SET_FOR_RANDOMIZING" размера выборки.
    Функция необходима для ускорения запросов к БД."""
    queryset = Question.objects.only(
        'question', 'answer', 'pass_criteria',
        'authors', 'sources', 'comments',
    ).filter(
        question_type=question_type,
        is_condemned=False,
        is_published=True
    )
    questions_quantity = get_max_question_sets()[question_type]
    randomizing_limit = questions_quantity - SET_FOR_RANDOMIZING - 1
    start_point = random.randint(
        0,
        randomizing_limit if randomizing_limit > 0 else questions_quantity
    )
    if questions_quantity < SET_FOR_RANDOMIZING:
        start_point = 0
    return queryset[start_point: start_point + SET_FOR_RANDOMIZING]


def get_pagination_obj(request, queryset, questions_displayed_on_page):
    """Функция для выноса общего кода пагинации страниц."""
    paginator = Paginator(
        queryset,
        questions_displayed_on_page
    )
    return paginator.get_page(request.GET.get('page'))
