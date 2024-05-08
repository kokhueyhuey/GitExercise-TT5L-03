from django.db import models
from django.contrib.auth.models import User
# import datetime

# Create your models here.
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
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

    def __str__(self):
        return self.name    