# Generated by Django 4.0.2 on 2022-04-30 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station_admin', '0028_alter_rentsession_taken_from_spot'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(default=370, max_length=50),
            preserve_default=False,
        ),
    ]
