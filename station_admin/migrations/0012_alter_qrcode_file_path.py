# Generated by Django 4.0.2 on 2022-03-12 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station_admin', '0011_qrcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='file_path',
            field=models.CharField(max_length=255),
        ),
    ]
