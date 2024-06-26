# Generated by Django 5.0.4 on 2024-06-05 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_booking_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='time',
            field=models.CharField(blank=True, choices=[('09:00', '9:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('14:00', '2:00'), ('15:00', '3:00'), ('16:00', '4:00'), ('17:00', '5:00'), ('full_day', 'Full (7:00-19:00)'), ('morning', 'Morning (7:00-12:00)'), ('noon', 'Noon (13:00-19:00)')], max_length=10, null=True),
        ),
    ]
