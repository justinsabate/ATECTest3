# Generated by Django 2.0.13 on 2019-09-12 18:23

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_client_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='mail',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='client',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
    ]