from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.questions, name='questions'),
    path(
        'telegram-bot/',
        TemplateView.as_view(template_name='questions/tg_bot.html'),
        name='tg-bot'
    ),
    path(
        'add/',
        views.add_question,
        name='add'
    ),
]
