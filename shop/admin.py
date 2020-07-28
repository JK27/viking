from django.contrib import admin
from .models import Product, Category


# ------------------------------------- PRODUCT ADMIN
class ProductAdmin(admin.ModelAdmin):

    readonly_fields = ('id', 'article_number')

    list_display = (
        'id', 'article_number', 'name',
        'master_category', 'category',
        'price', 'discounted_price',
        'brand', 'image',
    )

    ordering = ('id',)


# ------------------------------------- CATEGORY ADMIN
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
