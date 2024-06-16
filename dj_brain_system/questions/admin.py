from django.contrib import admin

from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'is_condemned', 'is_published',)
    search_fields = (
        'package',
        'tour',
        'question_type',
        'question',
    )
    list_filter = ('question_type', 'is_published',)
    empty_value_display = 'Информации нет'
