# Generated by Django 4.0.2 on 2022-04-09 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('station_admin', '0021_vehicle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='current_spot',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='station_admin.rentspot'),
        ),
    ]
