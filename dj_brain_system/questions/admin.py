from django.contrib import admin

from .models import Questions


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'condemned', 'is_published',)
    search_fields = (
        'package',
        'tour',
        'question_type',
        'question',
    )
    list_filter = ('question_type', 'is_published',)
    empty_value_display = 'Информации нет'
