from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import SubscriptionLineItem


# --------------------------------------------------------- UPDATE ON SAVE
@receiver(post_save, sender=SubscriptionLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update subscription total on lineitem update/create
    """
    instance.subscription.update_total()


# --------------------------------------------------------- UPDATE ON DELETE
@receiver(post_delete, sender=SubscriptionLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update subscription total on lineitem delete
    """
    print('delete signal received')
    instance.subscription.update_total()
