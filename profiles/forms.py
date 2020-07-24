from django import forms
from .models import UserProfile


# --------------------------------------------------------- PROFILE FORM
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        # Sets autofocus to phone no field
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            # If field is not default_country ...
            if field != 'default_country':
                # ... and if field is required...
                if self.fields[field].required:
                    # ... adds a star to placeholder
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # Sets placeholder values to dict above
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Adds CSS class for styling
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            # Removes field labels
            self.fields[field].label = False
