from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'feedback_text',
        'date',
    )
    search_fields = ('name',)
    list_display_links = ('name',)
