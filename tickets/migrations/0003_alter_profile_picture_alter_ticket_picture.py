# Generated by Django 4.1 on 2022-09-30 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_alter_address_cep_alter_profile_phone_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='picture',
            field=models.ImageField(default='default_ticket.png', upload_to='ticket_pics/'),
        ),
    ]