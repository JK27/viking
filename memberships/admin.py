from django.contrib import admin
from .models import Category, Membership, UserMembership


# ------------------------------------- MEMBERSHIP ADMIN
class MembershipAdmin(admin.ModelAdmin):

    readonly_fields = ('id',)

    list_display = (
        'id', 'friendly_name', 'category',
        'stripe_price_id', 'price',
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

    readonly_fields = ('id',
                       'active', 'date',)

    list_display = ('id', 'user', 'membership', 'stripe_customer_id',
                    )

    fields = ('full_name', 'user', 'membership', 'email', 'phone_number',
              'street_address1', 'street_address2', 'postcode',
              'town_or_city', 'county', 'country',
              'date', 'stripe_subscription_id', 'active',)

    ordering = ('id',)


# ------------------------------------- SUBSCRIPTION ADMIN
# class SubscriptionAdmin(admin.ModelAdmin):

#     readonly_fields = ('user_membership', 'stripe_subscription_id',
#                        'active', 'date')

#     fields = ('user_membership', 'full_name', 'email', 'phone_number',
#               'street_address1', 'street_address2', 'postcode',
#               'town_or_city', 'county', 'country',
#               'date', 'stripe_subscription_id', 'active',)

#     list_display = ('user_membership', 'full_name', 'stripe_subscription_id',
#                     'date', 'active',)


admin.site.register(Membership, MembershipAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserMembership, UserMembershipAdmin)
# admin.site.register(Subscription, SubscriptionAdmin)
