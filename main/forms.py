from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Owner, Pet, Booking

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['username', 'email']

class OwnerUpdateForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['phone_number']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name','age','species','breed','profile_pic']

class BookingForm(forms.ModelForm):
    SERVICE_CHOICES = [
        ('Hair Grooming', 'Hair Grooming'),
        ('Bath and Dry', 'Bath and Dry'),
        ('Pet Hotel', 'Pet Hotel'),
        ('Pet Daycare', 'Pet Daycare'),
    ]
    service = forms.ChoiceField(choices=SERVICE_CHOICES)

    class Meta:
        model = Booking
        fields = ['pet', 'date', 'time','checkin','checkout', 'service']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'checkin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'checkout': forms.DateTimeInput(attrs={'type': 'datetime-local'}),


        }

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet'].queryset = Pet.objects.filter(owner=owner)

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        checkin = cleaned_data.get('checkin')
        checkout = cleaned_data.get('checkout')

        if service in ['Pet Hotel', 'Pet Daycare']:
            if not checkin:
                self.add_error('checkin', 'Check-in time is required for Pet Hotel and Pet Daycare services.')
            if not checkout:
                self.add_error('checkout', 'Check-out time is required for Pet Hotel and Pet Daycare services.')

        return cleaned_data    