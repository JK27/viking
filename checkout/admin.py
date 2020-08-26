from django.contrib import admin
from .models import Order, OrderLineItem


# --------------------------------------------------------- ORDER LINE ITEM
class OrderLineItemAdminInline(admin.TabularInline):
    """
    Allows to add and edit line items in admin from inside order model
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)   # Item total price is uneditable


# --------------------------------------------------------- ORDER ADMIN
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    # --- Fields calculated automatically by models
    readonly_fields = ('order_number', 'date', 'grand_total',
                       'original_shoppingbag', 'stripe_pid')

    # --- Specifies order of fields to match model
    fields = ('order_number', 'date', 'user_profile', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'grand_total',
              'original_shoppingbag', 'stripe_pid')

    # --- Restricts columns showing up in order list
    list_display = ('order_number', 'date', 'full_name',
                    'grand_total',)

    # --- Order in reverse chronological order with most recent at top
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
