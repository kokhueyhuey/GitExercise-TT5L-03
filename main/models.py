from django.db import models
from django.contrib.auth.models import User
import random
# import datetime

# Create your models here.

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        # return f"{self.id},{self.user},{self.email}"
        return self.user.username
    
    def save(self, *args, **kwargs):
        self.email = self.user.email
        super().save(*args, **kwargs)
    
class Pet(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.CASCADE)
    age = models.PositiveBigIntegerField()
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    profile_pic = models.ImageField(default="profile.jpg", null=True, blank=True)

    def __str__(self):
        return self.name    
    
class Room(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name    

    
class Booking(models.Model):
    owner = models.ForeignKey(Owner, null=True, on_delete=models.CASCADE)
    pet = models.ManyToManyField(Pet)
    room = models.ForeignKey(Room, null=True, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    TIME_CHOICES = [
        ('09:00', '9:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('14:00', '2:00'),
        ('15:00', '3:00'),
        ('16:00', '4:00'),
        ('17:00', '5:00'),
        ('full_day', 'Full (7:00-19:00)'),
        ('morning', 'Morning (7:00-12:00)'),
        ('noon', 'Noon (13:00-19:00)'),
    ]
    time = models.CharField(max_length=10, choices=TIME_CHOICES, blank=True, null=True)
    SERVICE_CHOICES = [
        ('Hair Grooming', 'Hair Grooming'),
        ('Bath and Dry', 'Bath and Dry'),
        ('Pet Hotel', 'Pet Hotel'),
        ('Pet Daycare', 'Pet Daycare'),
    ]
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ongoing')

    def __str__(self):
        return f'{self.owner.user.username} - {self.date} {self.time}'      
    
    checkin = models.DateField(null=True, blank=True)
    checkout = models.DateField(null=True, blank=True)

class Feedback(models.Model):
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Rating: {self.rating}, Comment: {self.comment}'

