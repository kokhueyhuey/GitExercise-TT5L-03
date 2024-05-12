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
        fields = ['name','age','species','breed']

class BookingForm(forms.ModelForm):
    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet'].queryset = owner.pet_set.all()
    class Meta:
        model = Booking
        fields = ['pet','date','time','service']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }