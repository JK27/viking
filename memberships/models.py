from django.conf import settings
from django.db import models

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


# ------------------------------------------ CATEGORIES
class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=20)
    friendly_name = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(null=False)
    category_slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


# ------------------------------------------ MEMBERSHIPS
class Membership(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    membership_type = models.CharField(max_length=30)
    friendly_name = models.CharField(max_length=40, null=False, blank=True)
    short_description = models.TextField(null=False)
    full_description = models.TextField(null=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stripe_price_id = models.CharField(max_length=40, null=False, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.membership_type
