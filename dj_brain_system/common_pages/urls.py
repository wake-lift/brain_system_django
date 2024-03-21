from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'common_pages'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='common_pages/main.html'),
        name='main'
    ),
    path(
        'legal/',
        TemplateView.as_view(template_name='common_pages/legal.html'),
        name='legal'
    ),
    path(
        'feedback/',
        views.feedback,
        name='feedback'
    ),
]
