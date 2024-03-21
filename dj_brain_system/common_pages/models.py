from django.db import models


class Feedback(models.Model):
    name = models.CharField(
        max_length=128,
    )
    email = models.EmailField(
        help_text='Если вы хотите, чтобы вам ответили - заполните это поле',
        blank=True
    )
    feedback_text = models.TextField(
        max_length=5000,
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата сообщения',
    )

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return self.email
