# Generated by Django 2.1 on 2018-10-06 19:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20181003_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergeolocation',
            name='tempo',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
