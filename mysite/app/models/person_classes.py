from django.db import models
from .general import General
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from .product_classes import Location,Product

class LanguagePerson (General):
    def __str__(self):
        return self.lang
    lang = models.CharField(default='ESPANOL',max_length=100)

    def get_cname(self):
        class_name = 'LanguagePerson'
        return class_name

class TypePerson(General):
    def __str__(self):
        return self.type
    type = models.CharField(default='CLIENTE',max_length=100)

    def get_cname(self):
        class_name = 'TypePerson'
        return class_name


class Person(General):
    def __str__(self):
        return '['+str(self.type)+'] '+self.name
    NIN = models.IntegerField(blank=True,null=True)#National identification number
    name = models.CharField(default='', max_length=100)
    fam_name = models.CharField(default='', max_length=100, blank=True, null=True)
    date_birth = models.DateField(null=True, blank=True)
    date_birth = models.DateField(null=True, blank=True)
    nationality = CountryField(null=True,blank=True)
    name_Hotel = models.TextField(default='',blank=True,null=True)
    detail_location = models.TextField(default='',blank=True,null=True)

    ### KEYS ###
    location = models.ManyToManyField(Location, blank=True)
    language = models.ManyToManyField(LanguagePerson, blank=True)
    type = models.ForeignKey(
        TypePerson,
        on_delete=models.PROTECT,
        blank=True,
    )
    product = models.ManyToManyField(Product, blank=True)

    def get_cname(self):
        class_name = 'Person'
        return class_name

class Mail(General):
    def __str__(self):
        return self.email
    email = models.EmailField(default='',)

    ### KEYS ###
    per = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    ) ### in order for a person to be able to have multiple Mails

    def get_cname(self):
        class_name = 'Mail'
        return class_name

class Phone(General):
    def __str__(self):
        return str(self.tel)
    tel = PhoneNumberField(default='')

    ### KEYS ###
    per = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )### in order for a person to be able to have multiple Phone numbers

    def get_cname(self):
        class_name = 'Phone'
        return class_name

