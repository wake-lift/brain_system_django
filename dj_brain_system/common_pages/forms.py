from captcha.fields import CaptchaField
from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    captcha = CaptchaField(
        label='',
        help_text='Введите текст, указанный на картинке. '
                  'Регистр не имеет значения.'
    )

    class Meta:
        model = Feedback
        fields = ('name', 'email', 'feedback_text',)
