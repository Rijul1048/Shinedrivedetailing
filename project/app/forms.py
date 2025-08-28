from django import forms
from .models import Booking
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class BookingForm(forms.ModelForm):
    vehicle_type = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
        error_messages={'required': 'Vehicle type is required.'}
    )
    service_type = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
        error_messages={'required': 'Service type is required.'}
    )
    package_type = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
        error_messages={'required': 'Package type is required.'}
    )
    full_name = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Full name is required.'}
    )
    mobile = forms.CharField(
        max_length=15,
        required=True,
        error_messages={'required': 'Mobile number is required.'}
    )
    email = forms.EmailField(
        required=False, # Email is not strictly required as per the template
        error_messages={'invalid': 'Please enter a valid email address.'}
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        error_messages={'required': 'Date is required.'}
    )
    special_requests = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )
    class Meta:
        model = Booking
        fields = [
            'vehicle_type',
            'service_type',
            'package_type',
            'full_name',
            'mobile',
            'email',
            'date',
            'special_requests',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to all fields
        for field_name, field in self.fields.items():

            default_classes = 'block w-full py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200'

            # Add pl-10 for fields with icons
            if field_name in ['full_name', 'mobile', 'email', 'date']:
                default_classes += ' pl-10'
            else:
                default_classes += ' px-4' # Default padding for others

            if field_name == 'special_requests':
                default_classes += ' pt-3' # Adjust padding for textarea with icon

            field.widget.attrs['class'] = default_classes

            if self.errors.get(field_name):
                field.widget.attrs['class'] = default_classes + ' border-red-500' # Add error border
            else:
                field.widget.attrs['class'] = default_classes

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if mobile and not mobile.strip().isdigit():
            raise forms.ValidationError("Mobile number should contain only digits.")
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError("Please enter a valid email address.")
        return email