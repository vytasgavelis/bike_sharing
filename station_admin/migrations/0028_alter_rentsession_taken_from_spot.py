# Generated by Django 4.0.2 on 2022-04-23 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('station_admin', '0027_vehicle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentsession',
            name='taken_from_spot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taken_from_spot', to='station_admin.rentspot'),
        ),
    ]
