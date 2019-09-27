# Generated by Django 2.0.13 on 2019-09-25 18:01

import address.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '0002_auto_20160213_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='General',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.TextField(choices=[('0', 'DISABLED'), ('1', 'ENABLED')], default='1')),
                ('creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modification', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('act', models.TextField(default='')),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='AttributeProduct',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('text', models.TextField(default='')),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='ImageProduct',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('alt', models.TextField(blank=True, default='')),
                ('short_title', models.CharField(default='', max_length=100)),
                ('description', models.TextField(default='')),
                ('URL', models.CharField(default='', max_length=1000)),
                ('image', models.ImageField(default='app/static/img/tortuga.jpg', upload_to='app/static/img/')),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='LanguagePerson',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('lang', models.CharField(default='ESPANOL', max_length=100)),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='LineReservation',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(default=django.utils.timezone.now)),
                ('cost_price', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('payment_guide', models.TextField(choices=[('P', 'PAID'), ('NP', 'NOT PAID')], default='NP')),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('address', address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.Address')),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('email', models.EmailField(default='', max_length=254)),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='PaymentReservation',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('price', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('NIN', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(default='', max_length=100)),
                ('fam_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('date_birth', models.DateField(blank=True, null=True)),
                ('nationality', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('name_Hotel', models.TextField(blank=True, default='', null=True)),
                ('detail_location', models.TextField(blank=True, default='', null=True)),
                ('language', models.ManyToManyField(blank=True, to='app.LanguagePerson')),
                ('location', models.ManyToManyField(blank=True, to='app.Location')),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('tel', phonenumber_field.modelfields.PhoneNumberField(default='', max_length=128, region=None)),
                ('per', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Person')),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='PriceProduct',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('year', models.IntegerField(choices=[(1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028)], default=2019)),
                ('net', models.DecimalField(decimal_places=3, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('rack', models.DecimalField(decimal_places=3, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('date_start_offer', models.DateField(default=django.utils.timezone.now)),
                ('date_end_offer', models.DateField(blank=True, null=True)),
                ('information', models.TextField(blank=True, null=True)),
                ('specialoffer_percent_discount', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('category', models.TextField(choices=[('N', 'NINOS'), ('A', 'ADULTOS')], default='A')),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('type', models.TextField(choices=[('SERVICE', 'SERVICE'), ('MERCHANDISE', 'MERCHANDISE')], default='SERVICE')),
                ('name', models.CharField(default='', max_length=1000)),
                ('description', models.TextField(default='')),
                ('attribute', models.ManyToManyField(blank=True, to='app.AttributeProduct')),
                ('image', models.ManyToManyField(blank=True, to='app.ImageProduct')),
                ('location', models.ManyToManyField(blank=True, to='app.Location')),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('text', models.CharField(max_length=100)),
                ('percentage', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='app.General')),
                ('number_reservation', models.AutoField(primary_key=True, serialize=False)),
                ('payment_state', models.TextField(choices=[('P', 'PAID'), ('W', 'WAITING FOR PAYMENT'), ('SB', 'STANDBY')], default='W')),
                ('more_info', models.TextField(blank=True, default='', null=True)),
                ('total_payments', models.IntegerField(null=True)),
                ('total_to_pay', models.IntegerField(null=True)),
                ('total_costs', models.IntegerField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='StockProduct',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('nb_shop', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('nb_stock', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('description', models.TextField(default='')),
                ('assigned_date', models.DateField(default=django.utils.timezone.now)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('cause', models.TextField(blank=True, null=True)),
                ('assigner_auto', models.CharField(blank=True, max_length=100, null=True)),
                ('task_state', models.TextField(choices=[('D', 'DONE'), ('TD', 'TODO'), ('SB', 'STANDBY')], default='TD')),
                ('assigned_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('text', models.TextField(default='')),
                ('percentage', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028)], default=2019)),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='TypePayment',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('type', models.CharField(default='CASH', max_length=100)),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='TypePerson',
            fields=[
                ('general_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.General')),
                ('type', models.CharField(default='CLIENTE', max_length=100)),
            ],
            bases=('app.general',),
        ),
        migrations.CreateModel(
            name='AgeDiscount',
            fields=[
                ('rate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.Rate')),
            ],
            bases=('app.rate',),
        ),
        migrations.CreateModel(
            name='RateDiscount',
            fields=[
                ('rate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.Rate')),
            ],
            bases=('app.rate',),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.StockProduct'),
        ),
        migrations.AddField(
            model_name='priceproduct',
            name='price_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Product'),
        ),
        migrations.AddField(
            model_name='priceproduct',
            name='tax_price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.Tax'),
        ),
        migrations.AddField(
            model_name='person',
            name='product',
            field=models.ManyToManyField(blank=True, to='app.Product'),
        ),
        migrations.AddField(
            model_name='person',
            name='type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='app.TypePerson'),
        ),
        migrations.AddField(
            model_name='paymentreservation',
            name='payment_reservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Reservation'),
        ),
        migrations.AddField(
            model_name='paymentreservation',
            name='type_payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.TypePayment'),
        ),
        migrations.AddField(
            model_name='mail',
            name='per',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Person'),
        ),
        migrations.AddField(
            model_name='linereservation',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='clientXperson', to='app.Person'),
        ),
        migrations.AddField(
            model_name='linereservation',
            name='guide',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lineXguide', to='app.Person'),
        ),
        migrations.AddField(
            model_name='linereservation',
            name='line_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lineXproduct', to='app.Product'),
        ),
        migrations.AddField(
            model_name='linereservation',
            name='line_reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineXreservation', to='app.Reservation'),
        ),
        migrations.AddField(
            model_name='linereservation',
            name='sell_price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineXprice', to='app.PriceProduct'),
        ),
        migrations.AddField(
            model_name='priceproduct',
            name='age_discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.AgeDiscount'),
        ),
        migrations.AddField(
            model_name='priceproduct',
            name='rate_discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.RateDiscount'),
        ),
    ]
