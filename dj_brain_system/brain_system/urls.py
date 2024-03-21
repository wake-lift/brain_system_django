from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from . import views

app_name = 'brain_system'

urlpatterns = [
    path(
        'operating-principle/',
        TemplateView.as_view(
            template_name='brain_system/operating_principle.html'
        ),
        name='operating'
    ),
    path(
        'electric-schematics/',
        TemplateView.as_view(template_name='brain_system/circuit.html'),
        name='circuit'
    ),
    path(
        'pcb/',
        TemplateView.as_view(template_name='brain_system/pcb.html'),
        name='pcb'
    ),
    path(
        'printed-parts/',
        TemplateView.as_view(template_name='brain_system/printed_parts.html'),
        name='printed'
    ),
    path(
        'bought-in-products/',
        cache_page(60 * 60)(views.ProductsListView.as_view()),
        name='bought'
    ),
    path(
        'firmware/',
        TemplateView.as_view(template_name='brain_system/firmware.html'),
        name='firmware'
    ),
    path(
        'export_model_to_ods/',
        views.export_model_to_ods,
        name='export_model_to_ods'
    ),
]
