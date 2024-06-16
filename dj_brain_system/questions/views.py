import random

from django.contrib.auth.decorators import login_required
from django.core.serializers import deserialize, serialize
from django.shortcuts import render

from .forms import QuestionAddForm, QuestionForm
from .models import Question
from .services import get_initial_queryset, get_pagination_obj


def questions(request):
    if request.method == 'POST':
        """Обработка запроса при отправке пользователем заполненной формы."""
        form = QuestionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['search_pattern']:
                questions = Question.objects.filter(
                    question_type=form.cleaned_data['question_type'],
                    question__contains=form.cleaned_data['search_pattern'],
                    is_condemned=False,
                    is_published=True
                )
            else:
                questions = get_initial_queryset(
                    form.cleaned_data['question_type']
                )
            questions_quantity = min(
                form.cleaned_data['questions_quantity'],
                questions.count()
            )
            questions = random.choices(questions, k=questions_quantity)
            """Для корректной работы пагинации необходимо, чтобы
            сгенерированный случайный пакет и параметры
            запроса сохранялись в djando session."""
            serialized_data = serialize('json', questions)
            form_form = {
                'question_type': form.cleaned_data['question_type'],
                'search_pattern': form.cleaned_data['search_pattern'],
                'questions_quantity': form.cleaned_data['questions_quantity'],
                'questions_displayed_on_page': form.cleaned_data[
                    'questions_displayed_on_page'
                ],
            }
            request.session['from_form'] = form_form
            request.session['queryset'] = serialized_data
            request.session[
                'questions_displayed_on_page'
            ] = form.cleaned_data['questions_displayed_on_page']
            page_obj = get_pagination_obj(
                request,
                questions,
                form.cleaned_data['questions_displayed_on_page']
            )
            context = {'form': form,
                       'queryset': questions,
                       'page_obj': page_obj}
        else:
            context = {'form': form}
    elif request.method == 'GET' and 'page' in request.GET:
        """Обработка запроса при перемещении пользователя по страницам.
        Выборка вопросов не генерируется заново, а извлекается из
        данных django session."""
        form = QuestionForm(request.session['from_form'])
        questions = []
        for obj in deserialize('json', request.session['queryset']):
            questions.append(obj.object)
        page_obj = get_pagination_obj(
            request,
            questions,
            request.session['questions_displayed_on_page']
        )
        context = {'form': form, 'queryset': questions, 'page_obj': page_obj}
    else:
        """Обработка запроса при первоначальном заходе на страницу."""
        form = QuestionForm()
        context = {'form': form}
    return render(request, 'questions/questions.html', context)


@login_required(login_url='login')
def add_question(request):
    if request.method == 'POST':
        form = QuestionAddForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            context['form_saved'] = True
    else:
        form = QuestionAddForm()
        context = {'form': form}
        context['form_saved'] = False
    return render(request, 'questions/add_question.html', context)
