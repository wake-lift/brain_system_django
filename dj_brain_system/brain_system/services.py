from .models import BoughtInProduct


def unite_rows_with_multiple_links(product_list: list[dict]) -> list[dict]:
    """Объединяет в одну строку продукты с несколькими ссылками на магазины.
    Ссылки переносятся в одну ячейку через перенос строки."""
    i = 0
    while i < len(product_list) - 1:
        if (
            product_list[i]['name']
            == product_list[i + 1]['name']
            and product_list[i]['unit__name']
            == product_list[i + 1]['unit__name']
        ):
            product_list[i + 1]['link_for_product__link'] += (
                '\n' + product_list[i]['link_for_product__link']
            )
            product_list.pop(i)
            i -= 1
        i += 1
    return product_list


def get_base_queryset():
    """Формирует базовую выборку продуктов из БД."""
    return BoughtInProduct.objects.select_related(
        'unit'
    ).prefetch_related(
        'link_for_product'
    ).order_by('unit')
