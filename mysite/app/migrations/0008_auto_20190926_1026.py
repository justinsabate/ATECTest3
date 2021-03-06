# Generated by Django 2.0.13 on 2019-09-26 16:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190926_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='linereservation',
            name='discounted',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='paymentreservation',
            name='payment_reservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paymentXreservation', to='app.Reservation'),
        ),
        migrations.AlterField(
            model_name='priceproduct',
            name='age_discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='agediscount', to='app.AgeDiscount'),
        ),
        migrations.AlterField(
            model_name='priceproduct',
            name='rate_discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ratediscount', to='app.RateDiscount'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='tax_price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reservationXtax', to='app.Tax'),
        ),
    ]
