from django.contrib import admin
from .models import Subscription


# --------------------------------------------------------- SUBSCRIPTION ADMIN
class SubscriptionAdmin(admin.ModelAdmin):

    readonly_fields = ('subscription_number', 'date', 'total',)

    # --- Specifies order of fields to match model
    fields = ('subscription_number', 'membership', 'date', 'first_name',
              'last_name', 'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'total',)

    # --- Restricts columns showing up in order list
    list_display = ('subscription_number', 'date', 'first_name',
                    'last_name', 'membership', 'total',)

    # --- Order in reverse chronological order with most recent at top
    ordering = ('-subscription_number',)


admin.site.register(Subscription, SubscriptionAdmin)
