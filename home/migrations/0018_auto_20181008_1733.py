# Generated by Django 2.1 on 2018-10-08 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_usergeolocation_tempo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregaativa',
            name='ciclista',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Ciclista'),
        ),
    ]
