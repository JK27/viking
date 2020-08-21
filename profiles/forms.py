from django import forms
from .models import UserProfile


# --------------------------------------------------------- PROFILE FORM
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Render all fields except user
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'profile_first_name': 'First Name',
            'profile_last_name': 'Last Name',
            'profile_email': 'Email',
            'profile_phone_number': 'Phone Number',
            'profile_postcode': 'Postal Code',
            'profile_town_or_city': 'Town or City',
            'profile_street_address1': 'Street Address 1',
            'profile_street_address2': 'Street Address 2',
            'profile_county': 'County, Council or State',
        }

        # Sets autofocus to phone no field
        self.fields['profile_first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            # If field is not profile_country ...
            if field != 'profile_country':
                # ... and if field is required...
                if self.fields[field].required:
                    # ... adds a star to placeholder
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # Sets placeholder values to dict above
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Adds CSS class for styling
            self.fields[field].widget.attrs['class'] = 'border-black profile-form-input'
            # Removes field labels
            self.fields[field].label = False
