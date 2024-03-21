from rest_framework import serializers

from questions.models import Questions


class QuestionsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = ('question', 'answer', 'pass_criteria',
                  'comments', 'authors', 'sources',)


class QuestionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = ('package', 'tour', 'number', 'question_type', 'question',
                  'answer', 'pass_criteria', 'authors', 'sources', 'comments',)


class QuestionRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = ('id', 'package', 'tour', 'number', 'question_type',
                  'question', 'answer', 'pass_criteria', 'authors',
                  'sources', 'comments',)


class RequestParamsSerializer(serializers.Serializer):
    question_type = serializers.ChoiceField(
        choices=['what-where-when', 'brain-ring', 'jeopardy',],
        required=False
    )
    search = serializers.CharField(
        min_length=3,
        required=False
    )
    questions_limit = serializers.IntegerField(
        min_value=1,
        max_value=200,
        required=False
    )
    refresh = serializers.BooleanField(
        required=False,
    )
    limit = serializers.IntegerField(
        min_value=1,
        max_value=36,
        required=False
    )
    offset = serializers.IntegerField(
        min_value=1,
        max_value=100,
        required=False
    )
