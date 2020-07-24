from django import forms
from .models import Order


# --------------------------------------------------------- ORDER FORM
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    # --- Custom __init__ method
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        # Custom placeholders
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        # Sets autofocus to full name field
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                # If field is required...
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