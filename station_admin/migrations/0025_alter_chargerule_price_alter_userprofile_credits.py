# Generated by Django 4.0.2 on 2022-04-11 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station_admin', '0024_rentsession_vehicle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargerule',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='credits',
            field=models.FloatField(default=0),
        ),
    ]
