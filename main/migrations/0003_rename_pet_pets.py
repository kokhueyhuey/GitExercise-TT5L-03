# Generated by Django 5.0.4 on 2024-05-08 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_pet'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pet',
            new_name='Pets',
        ),
    ]
