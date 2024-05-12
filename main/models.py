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
    SERVICE_CHOICES = (
        ('grooming', 'grooming'),
        ('boarding', 'boarding'),
        # Add more services as needed
    )
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)

    def __str__(self):
        return f'{self.owner.user.username} - {self.date} {self.time}'         