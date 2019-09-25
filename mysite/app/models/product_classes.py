from django.conf import settings
from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField
from .general import General

### USEFUL CODE ###

# FOREIGN KEY #
# staff = models.ForeignKey(
#     settings.AUTH_USER_MODEL,
#     on_delete=models.CASCADE,
# )

# MANYTOMANYFIELDS #
# client = models.ManyToManyField(Client)

# CHOICES #
# TARIFAS = [
#     ('A', 'Adultos'),
#     ('E', 'Estudiantes Ticos'),
#     ('G', 'Grupos'),
#     ('N', 'Ninos'),
# ]
# tarifa = models.TextField(choices=TARIFAS, default='A')

# OTHER USEFUL OBJECTS #
# phone_number = PhoneNumberField(blank=True)
# country = CountryField(blank=True)
# mail = models.EmailField(default='')

# SAVE #
# def save(self, *args, **kwargs):
#     super(Reservation, self).save(*args, **kwargs)


class AttributeProduct(General):
    def __str__(self):
        return str(self.text)
    text = models.TextField(default='')

    def get_cname(self):
        class_name = 'AttributeProduct'
        return class_name


class Location(General):
    def __str__(self):
        return str(self.address)
    address = AddressField(blank=True, null=True, on_delete=models.CASCADE)

    def get_cname(self):
        class_name = 'Location'
        return class_name



class StockProduct(General):
    def __str__(self):
        return "SHOP "+str(self.nb_shop)+" STOCK "+str(self.nb_stock)

    nb_shop = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    nb_stock = models.IntegerField(default=0,validators=[MinValueValidator(0)])

    def get_cname(self):
        class_name = 'StockProduct'
        return class_name


class ImageProduct(General):
    def __str__(self):
        return str(self.short_title)
    alt = models.TextField(default='', blank=True)
    short_title = models.CharField(max_length=100,default='')
    description = models.TextField(default='')
    URL = models.CharField(default='', max_length=1000)
    image = models.ImageField(upload_to='app/static/img/', default='app/static/img/tortuga.jpg')

    def get_cname(self):
        class_name = 'ImageProduct'
        return class_name


class Rate(General):
    def __str__(self):
        return self.text
    text = models.CharField(max_length=100)
    percentage = models.IntegerField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)])

    def get_cname(self):
        class_name = 'Rate'
        return class_name


class Product(General):

    def __str__(self):
        return self.type +' '+ self.name

    SERVICE = 'SERVICE'
    MERCHANDISE = 'MERCHANDISE'
    TYPE = [
        (SERVICE, 'SERVICE'),
        (MERCHANDISE, 'MERCHANDISE'),
    ]

    type = models.TextField(default='SERVICE',choices=TYPE)
    name = models.CharField(default='',max_length=1000)
    description = models.TextField(default='')

    ### KEYS ###

    attribute = models.ManyToManyField(AttributeProduct, blank=True)
    location = models.ManyToManyField(Location, blank=True)
    stock = models.ForeignKey(
        StockProduct,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    image = models.ManyToManyField(ImageProduct, blank=True)

    def get_cname(self):
        class_name = 'Product'
        return class_name


class PriceProduct(General):
    ### Prices In Dolars, it may be possible to get a "currency" object and to convert, if necessary

    def __str__(self):
        st = 'YEAR ' + str(self.year) + ' ' + 'PRICE ' + str(self.net-(self.net*self.percent_discount/100)) +'$ start'+ str(self.date_start_offer) + '-end' + str(self.date_end_offer)
        return st
    CATEGORY_CHOICES = [
        ('N', 'NINOS'),
        ('A','ADULTOS'),
    ]
    YEAR_CHOICES = []
    for r in range(1900, (datetime.datetime.now().year + 10)):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    net = models.DecimalField(default=0, max_digits=6, decimal_places=3, validators=[MinValueValidator(0.0)])
    rack = models.DecimalField(default=0, max_digits=6, decimal_places=3, validators=[MinValueValidator(0.0)])
    date_start_offer = models.DateField(default=timezone.now)
    date_end_offer = models.DateField(blank=True, null=True)
    information = models.TextField(blank=True, null=True)

    percent_discount = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    category = models.TextField(choices=CATEGORY_CHOICES, default='A')

    ### KEYS
    price_product = models.ForeignKey(
        Product,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def get_cname(self):
        class_name = 'PriceProduct'
        return class_name

