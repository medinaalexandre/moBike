# Generated by Django 2.1 on 2018-08-30 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_entregaativa'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregaativa',
            name='lng_entrega',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
