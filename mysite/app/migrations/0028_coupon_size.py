# Generated by Django 2.0.13 on 2019-10-04 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='size',
            field=models.TextField(blank=True, default='44', null=True),
        ),
    ]
