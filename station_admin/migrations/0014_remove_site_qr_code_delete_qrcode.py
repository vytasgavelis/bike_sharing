# Generated by Django 4.0.2 on 2022-03-13 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station_admin', '0013_site_qr_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='qr_code',
        ),
        migrations.DeleteModel(
            name='QrCode',
        ),
    ]
