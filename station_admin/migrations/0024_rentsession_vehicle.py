# Generated by Django 4.0.2 on 2022-04-10 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('station_admin', '0023_rentsession'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentsession',
            name='vehicle',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='station_admin.vehicle'),
            preserve_default=False,
        ),
    ]