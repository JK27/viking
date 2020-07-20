from django.db import models


# ------------------------------------------ CATEGORIES
class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


# ------------------------------------------ PRODUCTS
class Product(models.Model):

    ACCESSORIES = 'AC'
    CLOTHING = 'CL'
    FOOTWEAR = 'FW'
    ON_SALE = 'SA'
    MASTER_CATEGORIES = [
        (ACCESSORIES, 'Accessories'),
        (CLOTHING, 'Clothing'),
        (FOOTWEAR, 'Footwear'),
        (ON_SALE, 'On sale'),
    ]

    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    master_category = models.CharField(max_length=2, choices=MASTER_CATEGORIES,
                                       null=True, blank=True, default="")
    article_number = models.CharField(max_length=254, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=6, decimal_places=2,
                                           null=True)
    brand = models.CharField(max_length=20, default="")
    brand_logo_url = models.URLField(max_length=1024, null=True, blank=True)
    gender = models.CharField(max_length=10, default="Unisex")
    base_colour = models.CharField(max_length=20, null=True, blank=True)
    has_sizes = models.BooleanField(default=True, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
