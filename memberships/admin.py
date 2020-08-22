from django.contrib import admin
from .models import Category, Membership


# ------------------------------------- MEMBERSHIP ADMIN
class MembershipAdmin(admin.ModelAdmin):

    readonly_fields = ('id',)

    list_display = (
        'id', 'friendly_name', 'category',
        'price',
    )

    ordering = ('id',)


# ------------------------------------- CATEGORY ADMIN
class CategoryAdmin(admin.ModelAdmin):

    readonly_fields = ('id',)

    list_display = (
        'id', 'friendly_name', 'name',
    )

    ordering = ('id',)


admin.site.register(Membership, MembershipAdmin)
admin.site.register(Category, CategoryAdmin)
