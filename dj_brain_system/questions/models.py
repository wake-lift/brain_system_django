from django.db import models


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('Б', 'Брейн-ринг'),
        ('ДБ', 'Брейн-ринг (детский)'),
        ('И', 'Вопросы из интернета'),
        ('Л', 'Бескрылка'),
        ('Ч', 'Что-где-когда'),
        ('ЧБ', 'Что-где-когда (тренировки)'),
        ('ЧД', 'Что-где-когда (детский)'),
        ('Э', 'Эрудитка'),
        ('Я', 'Своя игра'),
    ]
    package = models.CharField(
        max_length=256,
        verbose_name='Пакет',
        blank=True,
        null=True
    )
    tour = models.CharField(
        max_length=256,
        verbose_name='Тур',
        blank=True,
        null=True
    )
    number = models.IntegerField(
        verbose_name='Номер вопроса в пакете',
        blank=True,
        null=True
    )
    question_type = models.CharField(
        choices=QUESTION_TYPE_CHOICES,
        max_length=2,
        verbose_name='Тип вопроса',
        default=QUESTION_TYPE_CHOICES[4]
    )
    question = models.TextField(
        verbose_name='Текст вопроса',
        db_index=True
    )
    answer = models.TextField(
        verbose_name='Ответ на вопрос',
    )
    pass_criteria = models.TextField(
        verbose_name='Критерий правильности ответа',
        blank=True,
        null=True
    )
    authors = models.TextField(
        verbose_name='Автор(ы) вопроса',
        blank=True,
        null=True
    )
    sources = models.TextField(
        verbose_name='Источник',
        blank=True,
        null=True
    )
    comments = models.TextField(
        verbose_name='Комментарий к ответу',
        blank=True,
        null=True
    )
    """Вопросы, которые не годятся для выдачи: содержат ссылку на изображение,
    угловые скобки, некодируемый набор символов и т.п."""
    is_condemned = models.BooleanField(
        verbose_name='Вопрос исключен из выдачи',
        default=False
    )
    is_published = models.BooleanField(
        verbose_name='Вопрос опубликован',
        default=False
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'вопросы из Базы'
        verbose_name_plural = 'Вопросы из Базы'

    def __str__(self):
        return f'{self.question[:75]} ...'
