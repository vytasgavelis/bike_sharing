# Generated by Django 4.0.2 on 2022-03-06 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station_admin', '0004_alter_site_gate_open_url_alter_site_lock_open_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingSpot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taken', models.BooleanField()),
                ('spot_type', models.CharField(choices=[('bike', 'Bike')], max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='site',
            name='gate_open_url',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='lock_open_url',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
