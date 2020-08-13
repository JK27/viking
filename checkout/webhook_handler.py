from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from shop.models import Product
from profiles.models import UserProfile

import json
import time


# --------------------------------------------------------- STRIPE WH HANDLER
class StripeWH_Handler:
    """ Handle Stripe webhooks """
    # ------------------------------------------- __init__ method
    def __init__(self, request):
        self.request = request

    # ------------------------------------------- Send confirmation email
    def _send_confirmation_email(self, order):
        """Send user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            # Context
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            # Context
            {'order': order,
             'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,    # from email
            [cust_email]                    # to email(s)
        )

    # ------------------------------------------- Handle event method
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    # ----------------------------------------- Handle payment intent succeeded
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        shoppingbag = intent.metadata.shoppingbag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the billing details
        for field, value in billing_details.address.items():
            if value == "":                   # Replace empty fields with None
                billing_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None      # Allows anonymous users to check out
        username = intent.metadata.username
        # If user is not anonymous, user is authenticated...
        if username != 'AnonymousUser':
            # ... get their profile using their username...
            profile = UserProfile.objects.get(user__username=username)
            # ... and if save info was selected...
            if save_info:
                # ... add info to their profile
                profile.profile_phone_number = billing_details.phone,
                profile.profile_country = billing_details.address.country,
                profile.profile_postcode = billing_details.address.postal_code,
                profile.profile_town_or_city = billing_details.address.city,
                profile.profile_street_address1 = billing_details.address.line1,
                profile.profile_street_address2 = billing_details.address.line2,
                profile.profile_county = billing_details.address.state,
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            """
            Will try to find the order five times over five seconds
            before giving up and creating the order itself.
            """
            try:
                order = Order.objects.get(
                    # looks up field to make exact match but case insensitive
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    country__iexact=billing_details.address.country,
                    postcode__iexact=billing_details.address.postal_code,
                    town_or_city__iexact=billing_details.address.city,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    county__iexact=billing_details.address.state,
                    grand_total=grand_total,
                    original_shoppingbag=shoppingbag,
                    stripe_pid=pid,
                )
                # If order is found it will break out of the loop
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        # If the order exists...
        if order_exists:
            self._send_confirmation_email(order)
            # ...it will return 200 response
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: \
                Verified order already in database',
                status=200)
        # If the order doesn't exist...
        else:
            order = None
            # ... it will create the order
            try:
                order = Order.objects.create(
                    full_name=billing_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    country=billing_details.address.country,
                    postcode=billing_details.address.postal_code,
                    town_or_city=billing_details.address.city,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    county=billing_details.address.state,
                    original_shoppingbag=shoppingbag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(shoppingbag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    # ------------------------------------------- Handle payment intent failed
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
