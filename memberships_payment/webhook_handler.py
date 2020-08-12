from django.http import HttpResponse
from django.conf import settings

from .models import Subscription, SubscriptionLineItem
from memberships.models import Membership

import json
import time


# --------------------------------------------------------- STRIPE WH HANDLER
class StripeWH_Handler:
    """ Handle Stripe webhooks """
    # ------------------------------------------- __init__ method
    def __init__(self, request):
        self.request = request

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
        membershipsbag = intent.metadata.membershipsbag
        # save_info = intent.metadata.save_info
        billing_details = intent.charges.data[0].billing_details
        subscription_total = round(intent.charges.data[0].amount / 100, 2)

        subscription_exists = False
        attempt = 1
        while attempt <= 5:
            """
            Will try to find the order five times over five seconds
            before giving up and creating the order itself.
            """
            try:
                subscription = Subscription.objects.get(
                    # looks up field to make exact match but case insensitive
                    last_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    country__iexact=billing_details.address.country,
                    postcode__iexact=billing_details.address.postal_code,
                    town_or_city__iexact=billing_details.address.city,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    county__iexact=billing_details.address.state,
                    subscription_total=subscription_total,
                    original_membershipsbag=membershipsbag,
                    stripe_pid=pid,
                )
                # If order is found it will break out of the loop
                subscription_exists = True
                break
            except Subscription.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if subscription_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: \
                Verified order already in database',
                status=200)
        else:
            subscription = None
            try:
                subscription = Subscription.objects.create(
                    last_name=billing_details.name,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    country=billing_details.address.country,
                    postcode=billing_details.address.postal_code,
                    town_or_city=billing_details.address.city,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    county=billing_details.address.state,
                    original_membershipsbag=membershipsbag,
                    stripe_pid=pid,
                )
                for item_id, quantity in json.loads(membershipsbag).items():
                    membership = Membership.objects.get(id=item_id)
                    subscription_line_item = SubscriptionLineItem(
                        subscription=subscription,
                        membership=membership,
                        quantity=quantity,
                    )
                    subscription_line_item.save()
            except Exception as e:
                if subscription:
                    subscription.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created subscription in webhook',
            status=200)

    # ------------------------------------------- Handle payment intent failed
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
