from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField(
        label='',
        help_text='Введите текст, указанный на картинке. '
                  'Регистр не имеет значения.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
