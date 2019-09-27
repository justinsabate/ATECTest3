from django.conf import settings
from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField
from .general import General
#from.reservation_classes import Tax
#from .person_classes import Person

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




class Tax(General):
    text = models.TextField(default='')
    percentage = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)])

    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year + 10)):
        YEAR_CHOICES.append((r, r))
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def get_cname(self):
        class_name = 'Tax'
        return class_name

    def __str__(self):
        return str(self.percentage)+'% '+str(self.year)

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
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    image = models.ManyToManyField(ImageProduct, blank=True)

    def get_cname(self):
        class_name = 'Product'
        return class_name




