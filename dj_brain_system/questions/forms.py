from django import forms
from django_bootstrap5.widgets import RadioSelectButtonGroup

from .models import Questions


class QuestionForm(forms.Form):
    CHOICES = (
        ('Ч', 'Что-Где-Когда'),
        ('Б', 'Брейн-ринг'),
        ('Я', 'Своя игра'),
    )
    question_type = forms.ChoiceField(
        choices=CHOICES,
        initial='Ч',
        label='Выберите тип вопроса',
        help_text='',
        widget=RadioSelectButtonGroup
    )
    search_pattern = forms.CharField(
        required=False,
        min_length=3,
        label='Поиск по тексту вопроса',
        help_text='не менее трех символов',
    )
    questions_quantity = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=100,
        initial=15,
        label='Количество вопросов',
        help_text='не более 100',
    )
    questions_displayed_on_page = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=36,
        initial=5,
        label='Вопросов на странице',
        help_text='не более 36',
    )


class QuestionAddForm(forms.ModelForm):

    class Meta:
        model = Questions
        fields = ('package', 'tour', 'number', 'question_type',
                  'question', 'answer', 'pass_criteria', 'authors',
                  'sources', 'comments',)
        widgets = {
            'pass_criteria': forms.Textarea(attrs={'rows': 5, 'cols': 15}),
            'comments': forms.Textarea(attrs={'rows': 5, 'cols': 15}),
            'authors': forms.Textarea(attrs={'rows': 5, 'cols': 15}),
            'sources': forms.Textarea(attrs={'rows': 5, 'cols': 15}),
        }
