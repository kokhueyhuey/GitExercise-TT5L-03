from django.db import models
from django.contrib.auth.models import User
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
    breed = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name    
    
class Booking(models.Model):
    owner = models.ForeignKey(Owner, null=True, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, null=True, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    time = models.TimeField(blank=False)
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