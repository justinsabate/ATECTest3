from django.db import models
from .general import General
from django.utils import timezone

from django_countries.fields import CountryField
from .product_classes import Location,Product

class LanguagePerson (General):
    def __str__(self):
        return self.lang
    lang = models.CharField(default='ESPANOL',max_length=100)

    def get_cname(self):
        class_name = 'LanguagePerson'
        return class_name

class TypePerson(General): ##ninos o adultos
    def __str__(self):
        return self.type
    type = models.CharField(default='CLIENTE',max_length=100)

    def get_cname(self):
        class_name = 'TypePerson'
        return class_name


