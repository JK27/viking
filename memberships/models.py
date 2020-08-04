from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import UserProfile

from datetime import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# ------------------------------------------ CATEGORIES
class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    friendly_name = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


# ------------------------------------------ MEMBERSHIPS
MEMBERSHIP_CHOICES = (
    ('Legend', 'lgn'),
    ('Pro', 'pro'),
    ('Basic', 'basic')
)


class Membership(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES,
                                       default='basic', max_length=30)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stripe_plan_id = models.CharField(max_length=40)
    slug = models.SlugField()

    def __str__(self):
        return self.membership_type


# ------------------------------------------ USER MEMBERSHIPS
class UserMembership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40, default='')
    membership = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

    def get_user_membership(self):
        return self.user.membership

    def post_save_usermembership_create(sender, instance, created,
                                        *args, **kwargs):
        user_membership, created = UserMembership.objects.get_or_create(
            user=instance)

        if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
            new_customer_id = stripe.Customer.create(email=instance.email)
            user_membership.stripe_customer_id = new_customer_id['id']
            user_membership.membership = Membership.objects.get()
            user_membership.save()

    post_save.connect(post_save_usermembership_create,
                      sender=settings.AUTH_USER_MODEL)


# ------------------------------------------ SUBSCRIPTIONS
class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.created)

    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.current_period_end)


# --------------------------------------------------- CREATE OR UPDATE PROFILE
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
