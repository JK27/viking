from django.db import models
from django.db.models import Sum

from allauth.account.forms import SignupForm
from django import forms

from django_countries.fields import CountryField

from memberships.models import Membership
from profiles.models import UserProfile


# --------------------------------------------------------- SUBSCRIPTION
class Subscription(models.Model):

    def create_subscription_number():
        last_subscription = Subscription.objects.all().order_by('id').last()
        if not last_subscription:
            return 'VG0001'
        subscription_number = last_subscription.subscription_number
        subscription_int = int(subscription_number.split('VG')[-1])
        new_subscription_int = subscription_int + 1
        new_subscription_number = 'VG000' + str(new_subscription_int)
        return new_subscription_number

    subscription_number = models.CharField(max_length=6,
                                           default=create_subscription_number,
                                           null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True,  # Allows anonymous users to purchase
                                     related_name='subscriptions')
    first_name = models.CharField(max_length=50, null=False, blank=False,
                                  default="")
    last_name = models.CharField(max_length=50, null=False, blank=False,
                                 default="")
    email = models.EmailField(max_length=254, null=False, blank=False,
                              default="")
    phone_number = models.CharField(max_length=20, null=False, blank=False,
                                    default="")
    street_address1 = models.CharField(max_length=80, null=False,
                                       blank=False, default="")
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False,
                                    default="")
    postcode = models.CharField(max_length=20, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    # Sets Subscription date and time
    date = models.DateField(auto_now_add=True)
    subscription_total = models.DecimalField(max_digits=10,
                                             decimal_places=2,
                                             null=False, default=0)
    dd_account_no = models.CharField(max_length=8, null=False, blank=False)
    dd_sortcode = models.CharField(max_length=8, null=False, blank=False)
    # Original bag that created the order
    original_membershipsbag = models.TextField(null=False, blank=False,
                                               default='')
    # PaymentIntent id
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    # ------------------------------------------- Custom save method
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the subscription number
        if it hasn't been set already.
        """
        if not self.subscription_number:
            self.subscription_number = self.subscription_number()
        super().save(*args, **kwargs)

    # ------------------------------------------- Update total method
    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.subscription_total = self.subscriptionlineitems.aggregate(Sum('subscriptionlineitem_total'))['subscriptionlineitem_total__sum'] or 0
        self.save()

    def __str__(self):
        return self.subscription_number


# ------------------------------------------ SUBSCRIPTION LINE ITEM
class SubscriptionLineItem(models.Model):
    subscription = models.ForeignKey(Subscription, null=False, blank=False,
                                     on_delete=models.CASCADE,
                                     related_name='subscriptionlineitems')
    membership = models.ForeignKey(Membership, null=False, blank=False,
                                   on_delete=models.CASCADE)

    quantity = models.IntegerField(null=False, blank=False, default=1,)
    subscriptionlineitem_total = models.DecimalField(max_digits=6,
                                                     decimal_places=2,
                                                     null=False, blank=False,
                                                     editable=False)

    # --------------------------------- Custom save method
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.subscriptionlineitem_total = self.membership.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Membership {self.membership.friendly_name} \
            on subscription {self.subscription.subscription_number}'
