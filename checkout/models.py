import uuid     # Used to generate the order number

from django.db import models
from django.db.models import Sum

from django_countries.fields import CountryField

from shop.models import Product
from profiles.models import UserProfile


# --------------------------------------------------------- ORDER
class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False,
                                    editable=False)  # Automatically generated
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)  # Sets order date and time
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    # Original bag that created the order
    original_shoppingbag = models.TextField(null=False, blank=False,
                                            default='')
    # PaymentIntent id
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    # ------------------------------------------- Generate order number method
    def _generate_order_number(self):
        """
        Generate a random string of 32 characters,
        unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    # ------------------------------------------- Update total method
    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.grand_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.save()

    # ------------------------------------------- Custom save method
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


# --------------------------------------------------------- ORDER LINE ITEM
class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)

    # --------------------------------- Custom save method
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'article_number {self.product.article_number} \
            on order {self.order.order_number}'
