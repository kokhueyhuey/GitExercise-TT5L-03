# Generated by Django 5.0.4 on 2024-05-15 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_booking_pet_booking_pet'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='checkin',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='checkout',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
