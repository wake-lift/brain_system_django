from django.db import models


class Unit(models.Model):
    """Таблица узлов, в которые входят покупные детали."""
    name = models.CharField(
        max_length=64,
        verbose_name='Название',
        help_text='Деталь входит в состав:'
    )

    class Meta:
        verbose_name = 'Покупная деталь в составе'
        verbose_name_plural = 'Покупные детали в составе'

    def __str__(self):
        return self.name


class BoughtInProduct(models.Model):
    """Основная таблица покупных деталей."""
    name = models.CharField(
        max_length=64,
        verbose_name='Название',
        help_text='Название детали',
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        verbose_name='В составе',
        related_name='product_as_a_part_of',
        null=True,
        help_text='Деталь входит в состав:',
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Количество:',
    )
    product_type = models.CharField(
        max_length=128,
        verbose_name='Тип',
        blank=True,
        help_text='Тип',
    )
    comment = models.CharField(
        max_length=512,
        verbose_name='Комментарий',
        blank=True,
        help_text='Комментрий',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Покупная деталь'
        verbose_name_plural = 'Покупные детали'

    def __str__(self):
        return self.name


class BoughtInProductLink(models.Model):
    """Таблица ссылок на покупные детали в интернет-магазинах."""
    product = models.ForeignKey(
        BoughtInProduct,
        on_delete=models.CASCADE,
        verbose_name='Объект ссылки',
        related_name='link_for_product',
        blank=True,
        null=True
    )
    link = models.URLField(
        max_length=300,
        verbose_name='URL-адрес',
        blank=True,
        null=True,
        help_text='Ссылка на деталь',
    )
    link_short_name = models.CharField(
        max_length=128,
        verbose_name='Короткое название ссылки',
        blank=True,
        null=True,
        help_text='Короткое название ссылки для таблицы на сайте',
    )

    class Meta:
        verbose_name = 'Ссылка на покупную деталь'
        verbose_name_plural = 'Ссылки на покупные детали'

    def __str__(self):
        return self.link_short_name
