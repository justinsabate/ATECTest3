from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import math

from .product_classes import Product,Tax
from .person_classes import LanguagePerson,TypePerson
from .general import General,get_all_logged_in_users,Action
from django.conf import settings
from django_countries.fields import CountryField
from .product_classes import Location,Product
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
#### persons


def get_user_type(obj):
    try :
        pers = Person.objects.get(user=obj)
        typ = TypePerson.objects.get(typeXper=pers)
        return typ.type
    except:
        print('no person linked to this username')
        return 'type UNDEFINED'


class Person(General):
    def __str__(self):
        return '['+str(self.type)+'] '+self.name

    user = models.OneToOneField(User, on_delete=models.SET_NULL,null=True, blank=True,related_name='userXperson')


    NIN = models.IntegerField(blank=True,null=True)#National identification number
    name = models.CharField(default='', max_length=100)
    fam_name = models.CharField(default='', max_length=100, blank=True, null=True)
    date_birth = models.DateField(null=True, blank=True)
    nationality = CountryField(null=True,blank=True)
    name_Hotel = models.TextField(default='',blank=True,null=True)
    detail_location = models.TextField(default='',blank=True,null=True)

    ### KEYS ###
    location = models.ManyToManyField(Location, blank=True)
    language = models.ManyToManyField(LanguagePerson, blank=True)
    type = models.ForeignKey(
        TypePerson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='typeXper'
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
        on_delete=models.SET_NULL,
        null=True,
        related_name='mailXper'
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
        on_delete=models.SET_NULL,
        null=True,
        related_name='phoneXper'
    )### in order for a person to be able to have multiple Phone numbers

    def get_cname(self):
        class_name = 'Phone'
        return class_name
##### fin de persons %%%


class Rate(General):

    def __str__(self):
        return self.text
    text = models.CharField(max_length=100)
    percentage = models.IntegerField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)])



    def get_cname(self):
        class_name = 'Rate'
        return class_name

class RateDiscount(Rate):
    def get_cname(self):
        class_name = 'RateDiscount'
        return class_name

    ### KEYS
    agency = models.ForeignKey(
        Person,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='rateXagency'
    )

class AgeDiscount(Rate):
    def get_cname(self):
        class_name = 'AgeDiscount'
        return class_name

class PriceProduct(General):
    ### Prices In Dolars, it may be possible to get a "currency" object and to convert, if necessary


    # CATEGORY_CHOICES = [
    #     ('N', 'NINOS'),
    #     ('A','ADULTOS'),
    # ]
    YEAR_CHOICES = []
    for r in range(1900, (datetime.datetime.now().year + 10)):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    net_AGENCIA =   models.FloatField(null=True,blank=True,default=0, validators=[MinValueValidator(0.0)])
    net_ATEC =  models.FloatField(null=True,blank=True,default=0, validators=[MinValueValidator(0.0)])
    rack = models.FloatField(null=True,default=0, validators=[MinValueValidator(0.0)])
    date_start_offer = models.DateField(default=timezone.now)
    date_end_offer = models.DateField(blank=True, null=True)
    information = models.TextField(blank=True, null=True)

    specialoffer_percent_discount = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    #category = models.TextField(choices=CATEGORY_CHOICES, default='A')

    ### KEYS
    age_discount = models.ForeignKey(
        AgeDiscount,
        on_delete=models.SET_NULL,
        null=True,
        related_name='agediscount'
    )

    rate_discount = models.ForeignKey(
        RateDiscount,
        on_delete=models.SET_NULL,
        null=True,
        related_name = 'ratediscount'
    )

    price_product = models.ForeignKey( ###change name
        Product,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        st = 'YEAR ' + str(self.year) + ' ' + 'PRICE ' + str(self.rack) + ' $' # str(self.net-(self.net*self.percent_discount/100)) +'$ start'+ str(self.date_start_offer) + '-end' + str(self.date_end_offer)
        return st
    def get_cname(self):
        class_name = 'PriceProduct'
        return class_name

class TypePayment(General):
    type = models.CharField(max_length=100, default='CASH')

    def get_cname(self):
        class_name = 'TypePayment'
        return class_name
    def __str__(self):
        return self.type

class Reservation(General):

    def updt_payment_state(self, *args, **kwargs): ### if a paymentstate is on stand by we will not do anything
        if self.payment_state != 'SB':
            all_lines = LineReservation.objects.filter(line_reservation=self)
            all_prices = PaymentReservation.objects.filter(payment_reservation=self)
            total_sell_price = 0
            total_payment_price = 0

            for e in all_lines:
                try:
                    e.discounted = e.get_discounted()
                    super(General, e).save(*args, **kwargs)
                    total_sell_price += e.discounted
                    print('sell price added to total')
                except:
                    print('No sell price for line'+str(e))

            for f in all_prices:
                total_payment_price += f.price

            # Update of payment and to pay
            self.total_payments = total_payment_price
            self.sub_total_to_pay = total_sell_price #subtotal without tax
            self.total_to_pay = self.sub_total_to_pay  # subtotal without tax

            # ### Tax payment
            # this_tax = Tax.objects.filter(reservationXtax=self)
            # self.total_to_pay = total_sell_price*(1+(this_tax[0].percentage/100))

            # Update of payment state
            if self.total_to_pay == total_payment_price:

                self.payment_state = 'P'
                print('changed reservation to paid')

                #return '[AUTOMATIC SAVE]'
            else:
                self.payment_state = 'W'
                print('changed reservation to waiting for payment')
                #return ''
            super(General, self).save(*args, **kwargs)


    PAYMENT_STATE = [
        ('P', 'PAID'),
        ('W', 'WAITING FOR PAYMENT'),
        ('SB', 'STANDBY'),
    ]

    number_reservation = models.AutoField(primary_key=True) # Auto incrementation, unique
    payment_state = models.TextField(choices=PAYMENT_STATE, default='W') ###has to be a readonly if sum payments is = to total
    more_info = models.TextField(default='',blank=True,null=True)
    total_payments = models.FloatField(null=True,blank=True,default=0, validators=[MinValueValidator(0.0)])
    sub_total_to_pay =  models.FloatField(null=True,blank=True,default=0, validators=[MinValueValidator(0.0)])
    total_to_pay = models.FloatField(null=True,blank=True,default=0, validators=[MinValueValidator(0.0)])
    total_costs =  models.FloatField(null=True,blank=True,default=0, validators=[MinValueValidator(0.0)])


    ### KEYS
    user = models.ForeignKey( ### OR GET ALL LOGGED IN USERS? solamente persona de atec, el guia va a ser en las lignas
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True
        )
    tax_price = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reservationXtax'
    )



    def get_total_to_pay_RESERVATION(self):
        def round_up(n, decimals=0):
            multiplier = 10 ** decimals
            return math.ceil(n * multiplier) / multiplier
        lines = LineReservation.objects.filter(line_reservation=self)

        total = 0
        for line in lines:
            total += line.get_discounted()

        return round_up(total,2)


    def get_total_to_pay_CLIENT(self, lines):
        def round_up(n, decimals=0):
            multiplier = 10 ** decimals
            return math.ceil(n * multiplier) / multiplier

        total_to_pay = 0
        for line in lines:
            total_to_pay += line.get_discounted()

        total_to_pay = round_up(total_to_pay, 2)
        return total_to_pay



    def get_cname(self):
        class_name = 'Reservation'
        return class_name

    def __str__(self):
        return str(self.number_reservation)


class PaymentReservation(General):  ###created only when a client has paid
    price =  models.FloatField(null=True,blank=True,default=0, validators=[MinValueValidator(0.0)])
    date = models.DateTimeField(default=timezone.now)

    ### KEYS
    type_payment = models.ForeignKey(
        TypePayment,
        on_delete=models.SET_NULL,
        null=True
    )
    payment_reservation = models.ForeignKey(
        Reservation,
        on_delete=models.SET_NULL,
        null=True,
        related_name='paymentXreservation'
    )

    def get_cname(self):
        class_name = 'PaymentReservation'
        return class_name

    def updt_payment_state(self, *args, **kwargs): ### if a paymentstate is on stand by we will not do anything
        this_reservation = Reservation.objects.get(paymentXreservation=self)

        if this_reservation.payment_state != 'SB':
            all_lines = LineReservation.objects.filter(line_reservation=this_reservation)
            all_prices = PaymentReservation.objects.filter(payment_reservation=this_reservation)
            total_sell_price = 0
            total_payment_price = 0

            for e in all_lines:
                try:
                    e.discounted = e.get_discounted()
                    super(General, e).save(*args, **kwargs)
                    total_sell_price += e.discounted
                    print('sell price added to total')
                except:
                    print('No sell price for line'+str(e))

            for f in all_prices:
                total_payment_price += f.price

            # Update of payment and to pay
            this_reservation.total_payments = total_payment_price
            this_reservation.sub_total_to_pay = total_sell_price #subtotal without tax
            this_reservation.total_to_pay = this_reservation.sub_total_to_pay

            # ### Tax payment
            # this_tax = Tax.objects.filter(reservationXtax=this_reservation)
            # this_reservation.total_to_pay = total_sell_price*(1+(this_tax[0].percentage/100))

            # Update of payment state
            if total_sell_price == total_payment_price:

                this_reservation.payment_state = 'P'
                print('changed reservation to paid')

                #return '[AUTOMATIC SAVE]'
            else:
                this_reservation.payment_state = 'W'
                print('changed reservation to waiting for payment')
                #return ''
            super(General, this_reservation).save(*args, **kwargs)



    def __str__(self):
        return str(self.price)+' '+str(self.date)




class LineReservation(General):
    PAYMENT_CHOICES = [
        ('P','PAID'),
        ('NP', 'NOT PAID'),
    ]

    quantity = models.IntegerField(default=1,validators=[MinValueValidator(0)])
    date_start = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(null=True,blank=True)
    #cost_price = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    payment_guide = models.TextField(choices = PAYMENT_CHOICES, default='NP')
    # sell_price = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    discounted =  models.FloatField(null=True,blank=True,default=0, validators=[MinValueValidator(0.0)])
    card_paypal = models.BooleanField(default=False)

    ###KEYS
    language_reservation = models.ForeignKey(
        LanguagePerson,
        on_delete=models.SET_NULL,
        related_name='languageXline',
        null=True
    )
    client = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name='clientXperson',
        null=True
    )
    line_reservation = models.ForeignKey( #CHANGE THE NAME
        Reservation,
        on_delete=models.SET_NULL,
        related_name='lineXreservation',
        null=True
    )

    guide = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name='lineXguide',
        null=True
    )
    sell_price = models.ForeignKey(
        PriceProduct,
        on_delete=models.SET_NULL,
        related_name='lineXprice',
        null=True
    )
    line_product = models.ForeignKey( #change the name AND SELECT THE PRODUCTS OF THE GUIDE ONLY
        Product,
        on_delete=models.SET_NULL,
        related_name='lineXproduct',
        null=True
    )

    def get_product_name(self):
        product = Product.objects.get(lineXproduct=self)
        return product.name

    def get_client_name(self):
        client = Person.objects.get(clientXperson=self)
        return client.name+' '+client.fam_name


    def get_client_infos_or_agency(self):
        ####look for client or agency
        price = PriceProduct.objects.get(lineXprice=self)
        rate = RateDiscount.objects.get(ratediscount=price)

        try:
            agency = Person.objects.get(rateXagency=rate)
            client = agency

        except:
            client = Person.objects.get(clientXperson=self)



        ###get its informations
        try :
            phone = Phone.objects.get(per=client)
            ph='Phone: ' + str(phone.tel)
        except:
            ph=''
        try:
            email = Mail.objects.get(per=client)
            em=' Email: ' + str(email.email)
        except:
            em=''
        try:
            type = TypePerson.objects.get(typeXper=client)
            ty= ' Customer Type: ' + type.type
        except:
            ty=''
        st = ph+em+ty

        return st

    def get_client_name_or_agency(self):
        price = PriceProduct.objects.get(lineXprice=self)
        rate = RateDiscount.objects.get(ratediscount=price)

        try:
            agency = Person.objects.get(rateXagency=rate)
            return agency.name
        except:
            return self.get_client_name()


    def get_guide_name(self):
        guide = Person.objects.get(lineXguide=self)
        return guide.name+' '+guide.fam_name

    def get_language(self):
        #client = self.client
        client = Person.objects.get(clientXperson=self)
        language = LanguagePerson.objects.get(person=client)
        return language.lang

    def get_agediscount_name(self):
        disc = AgeDiscount.objects.get(agediscount=self.sell_price)
        if disc.text == 'ADULTOS':
            return disc.text
        else:
            return disc.text + ' (-'+str(disc.percentage)+'%)'

### Pour le calcul des prix sans taxes


    def get_discounted(self): ### à aligner avec self.discounted
        #price = PriceProduct.objects.get(lineXprice=self)
        def round_up(n, decimals=0):
            multiplier = 10 ** decimals
            return math.ceil(n * multiplier) / multiplier
        rack = self.get_rack()
        age = self.get_agediscount()
        rate = self.get_ratediscount()
        special = self.get_specialdiscount()

        total = self.quantity*((((1-rate/100)*rack)*(1-age/100))*(1-special/100))
        if self.card_paypal:
            total = total*1.07
        return round_up(total,2)

    def get_agediscount(self):
        disc = AgeDiscount.objects.get(agediscount=self.sell_price)
        return disc.percentage

    def get_specialdiscount(self):
        price = PriceProduct.objects.get(lineXprice=self)
        return price.specialoffer_percent_discount

    def get_rack(self):
        price = PriceProduct.objects.get(lineXprice=self)
        return price.rack*(1+self.get_tax()/100)

    def get_unit_price(self):
        def round_up(n, decimals=0):
            multiplier = 10 ** decimals
            return math.ceil(n * multiplier) / multiplier
        rack = self.get_rack()
        rate = self.get_ratediscount()
        return round_up(rack*(1-rate/100),4)

    def get_ratediscount(self):
        disc = RateDiscount.objects.get(ratediscount=self.sell_price)
        return disc.percentage

    def get_tax(self):
        res = Reservation.objects.get(lineXreservation=self)
        tax_object = Tax.objects.get(reservationXtax=res)
        return tax_object.percentage

    # def get_total_price(self):
    #     return self.discounted

    def get_discount(self):
        def round_up(n, decimals=0):
            multiplier = 10 ** decimals
            return math.ceil(n * multiplier) / multiplier
        if self.get_agediscount()==0 and self.get_specialdiscount()==0:
            return 0
        else:
            return round_up(self.quantity*self.get_unit_price()-self.get_discounted()+self.get_card_paypal(),4)
### fin du calcul des prix

    # def get_card_paypal(self):
    #     reservation = Reservation.objects.get(lineXreservation=self)
    #     return reservation.card_paypal
    #
    def get_card_paypal(self):
        def round_up(n, decimals=0):
            multiplier = 10 ** decimals
            return math.ceil(n * multiplier) / multiplier
        if self.card_paypal:
            total=self.get_discounted()*0.07
            return round_up(total, 4)
        else:
            return 0


    def __str__(self):
        return 'Line Reservation number ' +str(self.id)

    def get_cname(self):
        class_name = 'LineReservation'
        return class_name

    def updt_payment_state(self, *args, **kwargs): ### if a paymentstate is on stand by we will not do anything
        this_reservation = Reservation.objects.get(lineXreservation=self)
        if this_reservation.payment_state != 'SB':
            all_lines = LineReservation.objects.filter(line_reservation=this_reservation)
            all_prices = PaymentReservation.objects.filter(payment_reservation=this_reservation)
            total_sell_price = 0
            total_payment_price = 0

            for e in all_lines:
                try:
                    e.discounted = e.get_discounted()
                    super(General, e).save(*args, **kwargs)
                    total_sell_price += e.discounted
                    print('sell price added to total')
                except:
                    print('No sell price for line'+str(e))

            for f in all_prices:
                total_payment_price += f.price

            # Update of payment and to pay
            this_reservation.total_payments = total_payment_price
            this_reservation.sub_total_to_pay = total_sell_price #subtotal without tax
            this_reservation.total_to_pay = this_reservation.sub_total_to_pay
            # ### Tax payment
            # this_tax = Tax.objects.filter(reservationXtax=this_reservation)
            # this_reservation.total_to_pay = total_sell_price*(1+(this_tax[0].percentage/100))

            # Update of payment state
            if this_reservation.total_to_pay == total_payment_price:

                this_reservation.payment_state = 'P'
                print('changed reservation to paid')

                #return '[AUTOMATIC SAVE]'
            else:
                this_reservation.payment_state = 'W'
                print('changed reservation to waiting for payment')
                #return ''
            super(General, this_reservation).save(*args, **kwargs)


