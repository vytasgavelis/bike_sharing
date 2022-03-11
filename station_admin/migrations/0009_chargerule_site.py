# Generated by Django 4.0.2 on 2022-03-11 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('station_admin', '0008_chargerule_site_parking_charge_rule_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargerule',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='site', to='station_admin.site'),
        ),
    ]
