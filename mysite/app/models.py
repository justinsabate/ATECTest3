from django.conf import settings
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    # CLIENTS = [
    #     ('J', 'Justin'),
    #     ('Y', 'Yeral'),
    # ]

    TARIFAS = [
        ('A', 'Adultos'),
        ('E', 'Estudiantes Ticos'),
        ('G', 'Grupos'),
        ('N', 'Ninos'),
    ]

    name = models.CharField(max_length=100)  # ,maxlength=100)
    fam_name = models.CharField(max_length=100, default='')  # ,maxlength=100)
    tarifa = models.TextField(choices=TARIFAS, default='A')
    # phone_number = PhoneNumberField()
    # language = models.TextField(default='Language')
    # country = CountryField()
    # mail = models.EmailField(default='')
    ##res = models.CharField(max_length=100)


    ##reservations = []

    ##for e in reservations:
    ##    res=res+e


#    def __init__(self,n,fn,t):
#        self.name = n
#        self.fam_name = fn
#        self.tarifa = t
# self.country=CountryField()
# self.phone_number=PhoneNumberField()


#   def updateReservations(self):
#       for e in models.Reservation:
#           if e.client.name == self.name:
#               self.reservations.append(e)

#    def createclient(self):
#        Client.objects.create(country='CR')
#        self.save()

class Reservation(models.Model):
    TARIFAS = [
        ('A', 'Adultos'),
        ('E', 'Estudiantes Ticos'),
        ('G', 'Grupos'),
        ('N', 'Ninos'),
    ]

    ##from .models import Client
    numero = models.IntegerField()
    #name = models.CharField(max_length=100)

    CLIENTS = [('', '')]

    for e in Client.objects.all():
        CLIENTS.append((e.name, e.name))
    client = models.TextField(choices=CLIENTS, default='')

    ##def save(self, *args, **kwargs):
    ##    cl = Client.objects.get(name=self.client)
    ##    cl.reservations.append(self.numero)
    ##    super(Reservation, self).save(*args, **kwargs)

    # client = Client.object.create() #tentative de créer un nouveau client à partir d'une réservation

    # def assignClient(self):
    #    newclient = Client()
    #    self.client=newclient
    #    self.save()

    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # title = models.CharField(max_length=200)
    # text = models.TextField()
    # created_date = models.DateTimeField(default=timezone.now)
    # published_date = models.DateTimeField(blank=True, null=True)
    #
    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()
    #
    # def __str__(self):
    #     return self.title
