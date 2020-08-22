from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


# --------------------------------------------------------- USER PROFILE
class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    # Each user can only have one profile and...
    # ... only one profile can be attached to one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # All these fields come from Subscription model. All fields are optional
    profile_first_name = models.CharField(max_length=50, null=True,
                                          blank=True, default="")
    profile_last_name = models.CharField(max_length=50, null=True,
                                         blank=True, default="")
    profile_email = models.EmailField(max_length=254, null=True, blank=True,
                                      default="")
    profile_phone_number = models.CharField(max_length=20, null=True,
                                            blank=True, default="")
    profile_street_address1 = models.CharField(max_length=80, null=True,
                                               blank=True, default="")
    profile_street_address2 = models.CharField(max_length=80, null=True,
                                               blank=True)
    profile_town_or_city = models.CharField(max_length=40, null=True,
                                            blank=True, default="")
    profile_postcode = models.CharField(max_length=20, null=True, blank=True)
    profile_county = models.CharField(max_length=80, null=True, blank=True)
    profile_country = CountryField(blank_label='Country', null=True,
                                   blank=True)

    def __str__(self):
        return self.user.username


# --------------------------------------------------- CREATE OR UPDATE PROFILE
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile automatically each time
    the user object is saved.
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
