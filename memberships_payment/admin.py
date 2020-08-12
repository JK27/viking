from django.contrib import admin
from .models import Subscription, SubscriptionLineItem


# ----------------------------------------------- SUBSCRIPTION LINE ITEM
class SubscriptionLineItemAdminInline(admin.TabularInline):
    """
    Allows to add and edit line items in admin from inside subscription model
    """
    model = SubscriptionLineItem
    # Line item total price is uneditable
    readonly_fields = ('subscriptionlineitem_total',)


# --------------------------------------------------------- SUBSCRIPTION ADMIN
class SubscriptionAdmin(admin.ModelAdmin):

    inlines = (SubscriptionLineItemAdminInline,)

    readonly_fields = ('subscription_number', 'date', 'subscription_total',
                       'original_membershipsbag', 'stripe_pid')

    # --- Specifies order of fields to match model
    fields = ('subscription_number', 'date', 'first_name',
              'last_name', 'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'subscription_total',
              'dd_account_no', 'dd_sortcode',
              'original_membershipsbag', 'stripe_pid')

    # --- Restricts columns showing up in order list
    list_display = ('subscription_number', 'date', 'first_name',
                    'last_name', 'subscription_total',)

    # --- Order in reverse chronological order with most recent at top
    ordering = ('-date',)


admin.site.register(Subscription, SubscriptionAdmin)
