import pandas as pd
from django.http import FileResponse
from django.views.generic import ListView

from .models import BoughtInProduct
from .services import get_base_queryset, unite_rows_with_multiple_links


class ProductsListView(ListView):
    """Class for page with bought-in products table generation."""
    model = BoughtInProduct
    queryset = get_base_queryset()
    template_name = 'brain_system/bought_in_products.html'


def export_model_to_ods(request):
    product_list = list(
        get_base_queryset().values(
            'name',
            'a_part_of__name',
            'quantity',
            'product_type',
            'link_for_product__link',
            'comment'
        )
    )
    product_list = unite_rows_with_multiple_links(product_list)
    df = pd.DataFrame(product_list)
    df = df.rename(columns={
        'name': 'Название',
        'a_part_of__name': 'Входит в состав',
        'quantity': 'Кол-во',
        'product_type': 'Тип',
        'link_for_product__link': 'Ссылки',
        'comment': 'Комментарий'
    })
    with pd.ExcelWriter('static_dev/brain_system_BOM.ods',
                        engine='odf') as doc:
        df.to_excel(doc, sheet_name='Bought-in poducts')
    return FileResponse(
        open('static_dev/brain_system_BOM.ods', 'rb'),
        as_attachment=True
    )
