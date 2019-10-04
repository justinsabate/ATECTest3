# Generated by Django 2.0.13 on 2019-10-02 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20191002_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atec',
            name='image_1',
            field=models.ImageField(blank=True, default='ict.jpeg', null=True, upload_to='app/static/img'),
        ),
        migrations.AlterField(
            model_name='atec',
            name='image_2',
            field=models.ImageField(blank=True, default='codeofconduct.jpeg', null=True, upload_to='app/static/img'),
        ),
        migrations.AlterField(
            model_name='atec',
            name='image_3',
            field=models.ImageField(blank=True, default='fb.jpeg', null=True, upload_to='app/static/img'),
        ),
        migrations.AlterField(
            model_name='atec',
            name='image_4',
            field=models.ImageField(blank=True, default='tripadvisor.jpeg', null=True, upload_to='app/static/img'),
        ),
        migrations.AlterField(
            model_name='atec',
            name='image_5',
            field=models.ImageField(blank=True, default='turismosostenible.jpeg', null=True, upload_to='app/static/img'),
        ),
        migrations.AlterField(
            model_name='atec',
            name='logo',
            field=models.ImageField(blank=True, default='ATEC_LOGO.png', null=True, upload_to='app/static/img'),
        ),
    ]
