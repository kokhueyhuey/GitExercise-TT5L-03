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
    
    service = forms.ChoiceField(choices=SERVICE_CHOICES)
    time = forms.CharField(widget=forms.HiddenInput(), required=False)    

    class Meta:
        model = Booking
        fields = ['pet', 'date', 'time', 'checkin', 'checkout', 'service']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().strftime('%Y-%m-%d'), 'id': 'id_date'}),
            'checkin': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().strftime('%Y-%m-%d')}),
            'checkout': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().strftime('%Y-%m-%d')}),
        }

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet'].queryset = Pet.objects.filter(owner=owner)

        # Get the service and date from the initial data or POST data
        service = self.initial.get('service', self.data.get('service'))
        date = self.initial.get('date', self.data.get('date'))

        if service in ['Hair Grooming', 'Bath and Dry', 'Pet Daycare']:
            self.fields['time'].required = True
            self.fields['time'].choices = self.get_available_time_choices(date, service)
        else:
            self.fields['time'].required = False
            self.fields['time'].choices = [('', 'Select a time')]        
    def get_available_time_choices(self, date, service):
        if not date:
            # Return a default choice for the 'time' field when the 'date' is not provided
            return [('', 'Select a time')]

        if service == 'Hair Grooming' or service == 'Bath and Dry':
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
        elif service == 'Pet Daycare':
            TIME_CHOICES = [
                ('full_day', 'Full Day (7:00-19:00)'),
                ('morning', 'Morning (7:00-12:00)'),
                ('noon', 'Noon (13:00-19:00)'),
            ]
        else:
            TIME_CHOICES = []

        if not date:
            return TIME_CHOICES

        # Filter out fully booked times
        available_times = []
        for time in TIME_CHOICES:
            if service == 'Hair Grooming':
                limit = 2
            elif service == 'Bath and Dry':
                limit = 3
            elif service == 'Pet Daycare':
                if time[0] == 'full_day':
                    limit = 2
                elif time[0] == 'morning':
                    limit = 3
                elif time[0] == 'noon':
                    limit = 2
                else:
                    limit = float('inf')  # No limit for other services

            bookings = Booking.objects.filter(date=date, time=time[0], service=service)
            if bookings.count() < limit:
                available_times.append(time)

        return available_times
    
    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        checkin = cleaned_data.get('checkin')
        checkout = cleaned_data.get('checkout')

        if service in ['Pet Hotel']:
            if not checkin:
                self.add_error('checkin', 'Check-in time is required for Pet Hotel and Pet Daycare services.')
            if not checkout:
                self.add_error('checkout', 'Check-out time is required for Pet Hotel and Pet Daycare services.')
            cleaned_data['time'] = None

        pet = cleaned_data.get('pet')
        if pet and checkin and checkout:
            available_rooms = Room.objects.all()
            for room in available_rooms:
                overlapping_bookings = Booking.objects.filter(
                    room=room,
                    checkin__lt=checkout,
                    checkout__gt=checkin
                ).exists()

                if not overlapping_bookings:
                    self.cleaned_data['room'] = room
                    return cleaned_data
        
        return cleaned_data