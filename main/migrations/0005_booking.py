# Generated by Django 5.0.4 on 2024-05-09 04:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_owner_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('service', models.CharField(choices=[('service1', 'Service 1 Description'), ('service2', 'Service 2 Description'), ('service3', 'Service 3 Description')], max_length=50)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.owner')),
            ],
        ),
    ]
