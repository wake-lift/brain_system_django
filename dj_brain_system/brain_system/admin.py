from django.contrib import admin

from .models import (BoughtInProduct, BoughtInProductAsAPartOf,
                     BoughtInProductLink)


class BoughtInProductLinkInline(admin.StackedInline):
    model = BoughtInProductLink
    extra = 0


@admin.register(BoughtInProduct)
class BoughtInProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'a_part_of',
        'quantity',
        'product_type',
        'comment',
    )
    list_editable = (
        'a_part_of',
        'quantity',
        'product_type',
    )
    search_fields = ('name',)
    list_filter = ('a_part_of',)
    list_display_links = ('name',)
    inlines = (
        BoughtInProductLinkInline,
    )


@admin.register(BoughtInProductLink)
class BoughtInProductLinkAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'link',
        'link_short_name',
    )
    list_editable = (
        'link',
        'link_short_name',
    )
    list_display_links = ('product',)
    empty_value_display = 'Не задано'


@admin.register(BoughtInProductAsAPartOf)
class BoughtInProductAsAPartOfAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    list_filter = ('name',)
    list_display_links = ('name',)
    empty_value_display = 'Не задано'
