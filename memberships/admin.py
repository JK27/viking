from django.contrib import admin
from .models import Category, Membership, UserMembership


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


# ------------------------------------- USER MEMEBERSHIP ADMIN
class UserMembershipAdmin(admin.ModelAdmin):

    readonly_fields = ('id',)

    list_display = ('id', 'user', 'membership',)

    fields = ('user', 'membership',)

    ordering = ('id',)


admin.site.register(Membership, MembershipAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserMembership, UserMembershipAdmin)
