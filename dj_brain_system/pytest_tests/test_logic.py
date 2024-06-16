import pytest
from django.urls import reverse

from common_pages.models import Feedback
from questions.models import Question


@pytest.mark.django_db
def test_user_can_add_feedback(client, feedback_form_data):
    """
    Проверка того, что фидбек вностися в БД при отправке формы.
    """
    url = reverse('common_pages:feedback')
    client.post(url, data=feedback_form_data)
    assert Feedback.objects.count() == 1, (
        'Запись о фидбеке не была внесена в БД.'
    )
    feedback = Feedback.objects.get()
    assert feedback.name == feedback_form_data['name'], (
        'Содержимое поля "name" объекта фидбека, сохраненного в БД,'
        ' не соответствует ожидаемому.'
    )
    assert feedback.email == feedback_form_data['email'], (
        'Содержимое поля "email" объекта фидбека, сохраненного в БД,'
        ' не соответствует ожидаемому.'
    )
    assert feedback.feedback_text == feedback_form_data['feedback_text'], (
        'Содержимое поля "feedback_text" объекта фидбека, сохраненного в БД,'
        ' не соответствует ожидаемому.'
    )


@pytest.mark.django_db
def test_user_can_add_question(admin_client, question_add_form_data):
    """
    Проверка того, что новый вопрос вностися в БД при отправке формы.
    """
    url = reverse('questions:add')
    admin_client.post(url, data=question_add_form_data)
    assert Question.objects.count() == 1, (
        'Запись о новом вопросе не была внесена в БД.'
    )
    question = Question.objects.get()
    assert question.question_type == question_add_form_data['question_type'], (
        'Содержимое поля "question_type" объекта Question,'
        ' сохраненного в БД, не соответствует ожидаемому.'
    )
    assert question.question == question_add_form_data['question'], (
        'Содержимое поля "question" объекта Question,'
        ' сохраненного в БД, не соответствует ожидаемому.'
    )
    assert question.answer == question_add_form_data['answer'], (
        'Содержимое поля "answer" объекта Question,'
        ' сохраненного в БД, не соответствует ожидаемому.'
    )
    assert question.is_condemned is False, (
        'Содержимое поля "is_condemned" объекта Question,'
        ' сохраненного в БД, не соответствует дефолтному значению.'
    )
    assert question.is_published is False, (
        'Содержимое поля "is_published" объекта Question,'
        ' сохраненного в БД, не соответствует дефолтному значению.'
    )
