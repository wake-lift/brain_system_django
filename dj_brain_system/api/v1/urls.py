from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter

from api.v1.views import QuestionViewSet

app_name = 'api'

router_questions = SimpleRouter()
router_questions.register(
    r'questions',
    QuestionViewSet,
    basename='questions'
)

urlpatterns = [
    path(
        'info/',
        TemplateView.as_view(template_name='api/api_info.html'),
        name='info'
    ),
    path('', include(router_questions.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
