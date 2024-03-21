from django.core.serializers import deserialize, serialize
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from questions.models import Questions

from .serializers import (QuestionCreateSerializer, QuestionRetrieveSerializer,
                          QuestionsListSerializer, RequestParamsSerializer)
from .throttling import (AnonHourThrottle, AnonMinuteThrottle,
                         UserHourThrottle, UserMinuteThrottle)

QUESTION_TYPE_DICT = {
    'what-where-when': 'Ч',
    'brain-ring': 'Б',
    'jeopardy': 'Я',
    None: 'Ч'
}


class QuestionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'retrieve',]
    throttle_classes = [
        AnonHourThrottle,
        AnonMinuteThrottle,
        UserHourThrottle,
        UserMinuteThrottle,
    ]
    pagination_class = LimitOffsetPagination
    default_questions_limit = 5
    swagger_schema = None

    def get_serializer_class(self):
        if self.action == 'list':
            return QuestionsListSerializer
        if self.action == 'create':
            return QuestionCreateSerializer
        return QuestionRetrieveSerializer

    def get_permissions(self):
        if self.action == 'create':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        serializer = QuestionRetrieveSerializer(
            obj,
            context={'request': request}
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return get_object_or_404(Questions, pk=self.kwargs['pk'])

    def _get_base_queryset(self, question_type, questions_limit, search):
        """Формирует базовую выдачу с учетом параметров API-запроса."""
        queryset = Questions.objects.filter(
            condemned=False,
            is_published=True,
            question_type=QUESTION_TYPE_DICT[question_type],
        )
        if search:
            queryset = queryset.filter(question__contains=search)
        queryset = queryset.order_by('?')
        return queryset[:int(questions_limit) if questions_limit
                        else self.default_questions_limit]

    def get_queryset(self):
        incoming_params = RequestParamsSerializer(
            data=self.request.query_params
        )
        incoming_params.is_valid(raise_exception=True)
        question_type = self.request.query_params.get('question_type')
        questions_limit = self.request.query_params.get('questions_limit')
        search = self.request.query_params.get('search')
        if not self.request.query_params.get('limit'):
            """Обработка запроса в случае,
            если параметры пагинации не заданы."""
            queryset = self._get_base_queryset(
                question_type, questions_limit, search
            )
        else:
            """Обработка запроса с учетом пагинации.
            Выдача нового списка вопросов.
            Список сохраняется в django session."""
            if (
                not self.request.session.get('queryset')
                or self.request.query_params.get('refresh')
            ):
                queryset = self._get_base_queryset(
                    question_type, questions_limit, search
                )
                serialized_queryset = serialize('json', queryset)
                self.request.session['queryset'] = serialized_queryset
            else:
                """Обработка запроса с учетом пагинации.
                Перемещение по страницам.
                Список вопросов извлекается из данных django session."""
                queryset = [
                    obj.object for obj in deserialize(
                        'json', self.request.session['queryset']
                    )
                ]
        return queryset
