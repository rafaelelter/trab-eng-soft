# Generated by Django 4.1.1 on 2022-10-01 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0005_alter_offererapproval_approved_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="latitude",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="address",
            name="longitude",
            field=models.FloatField(blank=True, null=True),
        ),
    ]