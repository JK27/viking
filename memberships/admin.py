from django.contrib import admin
from .models import Category, Membership, UserMembership, Subscription


# ------------------------------------- MEMBERSHIP ADMIN
class MembershipAdmin(admin.ModelAdmin):

    readonly_fields = ('id',)

    list_display = (
        'id', 'category', 'membership_type',
        'friendly_name', 'price',
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

    list_display = ('id', 'user', 'membership',
                    )

    ordering = ('id',)


admin.site.register(Membership, MembershipAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserMembership, UserMembershipAdmin)
admin.site.register(Subscription)
