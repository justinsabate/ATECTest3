from django.conf import settings
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField

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

    CATEGORIAS = [
        ('C','Clientos'),
        ('A', 'Agencia'),
    ]

    id = models.IntegerField(unique=True,primary_key=True)
    name = models.CharField(max_length=100)  # ,maxlength=100)
    fam_name = models.CharField(max_length=100, default='')  # ,maxlength=100)
    tarifa = models.TextField(choices=TARIFAS, default='A')
    phone_number = PhoneNumberField(blank=True)
    country = CountryField(blank=True)
    mail = models.EmailField(default='')
    categoria = models.TextField(choices=CATEGORIAS,default='C')

    ##def __str__(self):
    ##    return self.name+self.fam_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ##CLIENTS = [('', '')]
        ##for e in Client.objects.all():
        ##    CLIENTS.append((e.name, e.name))
        super(Client, self).save(*args, **kwargs)

    # def get_all_Clients(self):
    #     cli = []
    #
    #     for e in Client.objects.all():
    #         cli.append(e.pk)
    #     return cli

    # phone_number = PhoneNumberField()
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
    # TARIFAS = [
    #     ('A', 'Adultos'),
    #     ('E', 'Estudiantes Ticos'),
    #     ('G', 'Grupos'),
    #     ('N', 'Ninos'),
    # ]

    ##from .models import Client

    #maxi = self.models.objects.order_by('numero')

    numero = models.IntegerField(unique=True)
    client = models.ManyToManyField(Client)
    ##client = models.IntegerField(unique=True,blank=True,default=0)

    #numero = maxi[-1]+1
    #name = models.CharField(max_length=100)

    ##CLIENTS = [('', '')]

    ##for e in Client.objects.all():
    ##    CLIENTS.append((e.name, e.name))
    ##client = models.TextField(choices=CLIENTS, default='')

    # CLIENTS = Client.get_all_Clients(object)
    # tup = []
    # for e in CLIENTS :
    #     obj = Client.objects.get(pk=e)
    #     tup.append((obj.name,obj.name))
    # client = models.TextField(choices=tup, default='')

    def __str__(self):
        return str(self.numero)

    def save(self, *args, **kwargs):

        super(Reservation, self).save(*args, **kwargs)

    ##def link(self):
    ##    self.client = object.filter(Client.id == Reservation.numero)
    ##    self.save()
    # def save(self, *args, **kwargs):
    #     #cl = Client.objects.get(name=self.client)
    #     #cl.reservations.append(self.numero)
    #     super(Reservation, self).save(*args, **kwargs)

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

class Tarea(models.Model):

    ESTADOS = [
        ('R','Realizada'),
        ('NR', 'No Realizada'),
        ('SB', 'Stand By'),
        ('A', 'Esperando el Administrador que debe hacerla'),
        ('G', 'Esperando la repuesta del guia'),
    ]
    estado = models.TextField(choices=ESTADOS,default='NR')
    guia = models.CharField(blank=True,max_length=100)

    staff = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
        )

class Servicio(models.Model):

    DIFFICULTAD = [
        ('D','Dificil'),
        ('N','Normal'),
        ('F','Facil'),
    ]

    Nombre = models.CharField(max_length=1000)
    Precio = models.PositiveIntegerField(default=0)
    Duracion = models.DurationField(default=0)
    Dificultad = models.TextField(default='Normal',choices=DIFFICULTAD)
    Incluyo = models.TextField(default='')
    Localizacion = models.TextField(default='')
    #Localizacion = AddressField(on_delete=models.CASCADE) #un peu trop complet, à affiner

    Description = models.TextField(default='')
    image = models.ImageField(upload_to='app/static/img',default='app/static/img/header-bg.jpg')
    #Tours = # have to create a foreignkey with the future class tours