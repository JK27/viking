from django import forms
from allauth.account.forms import SignupForm

from django_countries.fields import CountryField

# from .models import UserProfile


class SubscriptionForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    phone_number = forms.CharField(max_length=20)
    street_address1 = forms.CharField(max_length=80)
    street_address2 = forms.CharField(max_length=80, required=False)
    town_or_city = forms.CharField(max_length=40)
    postcode = forms.CharField(max_length=20)
    county = forms.CharField(max_length=80, required=False)
    country = CountryField(blank_label='Country *').formfield()

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.street_address1 = self.cleaned_data['street_address1']
        user.street_address2 = self.cleaned_data['street_address2']
        user.town_or_city = self.cleaned_data['town_or_city']
        user.postcode = self.cleaned_data['postcode']
        user.county = self.cleaned_data['county']
        user.country = self.cleaned_data['country']
        user.save()
        return user

    # --- Custom __init__ method
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        # Custom placeholders
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email address',
            'email2': 'Confirm email address',
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm password',
            'phone_number': 'Phone number',
            'street_address1': 'Address',
            'street_address2': 'Address (continuation)',
            'town_or_city': 'Town or city',
            'postcode': 'Postcode',
            'county': 'County, council or state',
            'country': 'Country',
        }

        # Sets autofocus to first name field
        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            # If field is not country...
            if field != 'country':
                # ...and if field is required...
                if self.fields[field].required:
                    # ... adds a star to placeholder
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # Sets placeholder values to dict above
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Adds CSS class for styling
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Removes field labels
            self.fields[field].label = False

# --------------------------------------------------------- SUBSCRIPTION FORM
# class SubscriptionForm(forms.ModelForm):

    # class Meta:
    #     model = Subscription
    #     fields = ('first_name', 'last_name', 'email', 'phone_number',
    #               'street_address1', 'street_address2',
    #               'town_or_city', 'postcode', 'county', 'country',
    #               'dd_account_no', 'dd_sortcode',)

    # # --- Custom __init__ method
    # def __init__(self, *args, **kwargs):
    #     """
    #     Add placeholders and classes, remove auto-generated
    #     labels and set autofocus on first field
    #     """
    #     super().__init__(*args, **kwargs)
    #     # Custom placeholders
    #     placeholders = {
    #         'first_name': 'First Name',
    #         'last_name': 'Last Name',
    #         'email': 'Email Address',
    #         'phone_number': 'Phone Number',
    #         'street_address1': 'Street Address 1',
    #         'street_address2': 'Street Address 2',
    #         'town_or_city': 'Town or City',
    #         'postcode': 'Postcode',
    #         'county': 'County, Council or State',
    #         'dd_account_no': '12345678',
    #         'dd_sortcode': '00-00-00',
    #     }

    #     # Sets autofocus to first name field
    #     self.fields['first_name'].widget.attrs['autofocus'] = True
    #     for field in self.fields:
    #         # If field is not country...
    #         if field != 'country':
    #             # ...and if field is required...
    #             if self.fields[field].required:
    #                 # ... adds a star to placeholder
    #                 placeholder = f'{placeholders[field]} *'
    #             else:
    #                 placeholder = placeholders[field]
    #             # Sets placeholder values to dict above
    #             self.fields[field].widget.attrs['placeholder'] = placeholder
    #         # Adds CSS class for styling
    #         self.fields[field].widget.attrs['class'] = 'stripe-style-input'
    #         # Removes field labels
    #         self.fields[field].label = False
