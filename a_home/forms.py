from django import forms
from a_users.models import Individual,Group
import re
from django.core.exceptions import ValidationError

class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = [
            'firstname', 'surname', 'email', 'phone', 'address', 'city',
            'dob', 'position'
        ]
        widgets = {
            'firstname': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Enter surname'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter city'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select date of birth'}),
            'position': forms.TextInput(attrs={'placeholder': 'Enter position'}),
        }
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        phone_cleaned = phone.replace("+", "")

        pattern_263 = r"^2637[1378]\d{8}$"  # Must be 12 digits and start with 2637
        pattern_07 = r"^07[1378]\d{7}$"     # Must be 10 digits and start with 07

        # Validate phone number format
        if phone.startswith('+2637') or phone.startswith('2637'):
            phone_cleaned = phone_cleaned.replace('+', '')
            if not re.match(pattern_263, phone_cleaned):
                if len(phone_cleaned) != 12:
                    raise ValidationError('Invalid phone number: should start with 2637 and be 12 digits long.')
        elif phone.startswith('07'):
            if not re.match(pattern_07, phone):
                raise ValidationError('Invalid phone number: should start with 07 and be 10 digits long.')
        else:
            raise ValidationError('Invalid phone number format.')

        return phone

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        
        widgets ={
            'name': forms.TextInput(attrs={'placeholder': 'Enter group name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter group description'})
        }
