# Generated by Django 4.1 on 2022-10-01 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_alter_profile_picture_alter_ticket_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='expiration',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchases', to='tickets.profile'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='offerer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='tickets.profile'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='picture',
            field=models.ImageField(default='default_ticket.png', upload_to='ticket_pics'),
        ),
    ]