from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

    """
    Overrides the ready method and imports custom signals module.
    Every time a line item is saved or deleted,
    custom update total model method will be called
    """
    def ready(self):
        import checkout.signals
