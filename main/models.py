from django.db import models

class BookingDetails(models.Model):
    service = models.CharField(max_length=50)
    time_slot = models.DateTimeField(max_length=100)
    number_of_pets = models.CharField(max_length=100)
    date = models.DateField(max_length=100)