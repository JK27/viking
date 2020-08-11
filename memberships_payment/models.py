from django.db import models
from memberships.models import Membership

from django_countries.fields import CountryField


# --------------------------------------------------------- SUBSCRIPTION
class Subscription(models.Model):

    def create_subscription_number():
        last_subscription = Subscription.objects.all().order_by('id').last()
        if not last_subscription:
            return 'VG0001'
        subscription_number = last_subscription.subscription_number
        subscription_int = int(subscription_number.split('VG')[-1])
        new_subscription_int = subscription_int + 1
        new_subscription_number = 'VG' + str(new_subscription_int)
        return new_subscription_number

    subscription_number = models.CharField(max_length=6,
                                           default=create_subscription_number,
                                           null=False, editable=False)
    membership = models.ForeignKey(Membership, null=False, blank=False,
                                   on_delete=models.CASCADE)
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
    date = models.DateTimeField(auto_now_add=True)  # Sets order date and time
    total = models.DecimalField(max_digits=10, decimal_places=2,
                                null=False, default=0)

    # ------------------------------------------- Custom save method
    # def save(self, *args, **kwargs):
    #     """
    #     Override the original save method to set the subscription number
    #     if it hasn't been set already.
    #     """
    #     if not self.subscription_number:
    #         self.subscription_number = self.subscription_number()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.subscription_number
