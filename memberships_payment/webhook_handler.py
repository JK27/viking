from django.http import HttpResponse


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
        print(intent)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}  SUCCESS: Created order in webhook',
            status=200)

    # ------------------------------------------- Handle payment intent failed
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
