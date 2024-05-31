from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Owner, Pet, Booking, Room
from django.utils import timezone

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

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']

class BookingForm(forms.ModelForm):
    SERVICE_CHOICES = [
        ('Hair Grooming', 'Hair Grooming'),
        ('Bath and Dry', 'Bath and Dry'),
        ('Pet Hotel', 'Pet Hotel'),
        ('Pet Daycare', 'Pet Daycare'),
    ]
    TIME_CHOICES = [
        ('09:00', '9:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('14:00', '2:00'),
        ('15:00', '3:00'),
        ('16:00', '4:00'),
        ('17:00', '5:00'),
    ]
    service = forms.ChoiceField(choices=SERVICE_CHOICES)
    time = forms.ChoiceField(choices=TIME_CHOICES)
    
    class Meta:
        model = Booking
        fields = ['pet', 'date', 'time', 'checkin', 'checkout', 'service']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'in': timezone.now().date().strftime('%Y-%m-%d')}),
            'checkin': forms.DateInput(attrs={'type': 'date', 'in': timezone.now().date().strftime('%Y-%m-%d')}),
            'checkout': forms.DateInput(attrs={'type': 'date', 'in': timezone.now().date().strftime('%Y-%m-%d')}),
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

        pet = cleaned_data.get('pet')
        if pet and checkin and checkout:
            available_rooms = Room.objects.all()
            for room in available_rooms:
                overlapping_bookings = Booking.objects.filter(
                    room=room,
                    checkin__lt=checkout,
                    checkout__gt=checkin
                ).exists()

                if not overlapping_bookings :
                    self.cleaned_data['room'] = room
                    return cleaned_data

        
        return cleaned_data