# Generated by Django 2.0.13 on 2019-10-02 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20191002_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atec',
            name='logo',
            field=models.ImageField(blank=True, default='img/ATEC_LOGO.png', null=True, upload_to=''),
        ),
    ]
