# Generated by Django 2.0.13 on 2019-10-03 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20191003_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='card_paypal',
            field=models.BooleanField(default=False),
        ),
    ]
