

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_booking_date_alter_booking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='breed',
            field=models.CharField(max_length=50),
        ),
    ]
