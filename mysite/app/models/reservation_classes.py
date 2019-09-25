from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


from .product_classes import PriceProduct,Product,Rate
from .person_classes import Person
from .general import General
from django.conf import settings

import datetime

class TypePayment(General):
    type = models.CharField(max_length=100, default='CASH')

    def get_cname(self):
        class_name = 'TypePayment'
        return class_name
    def __str__(self):
        return self.type

class Reservation(General):

    def updt_payment_state(self, *args, **kwargs): ### (doubled the function to be able to use self.thisfunction in general where we cant import those classes (circular import) if a paymentstate is on stand by we will not do anything
        if self.payment_state != 'SB':
            all_lines = LineReservation.objects.filter(line_reservation=self)
            all_prices = PaymentReservation.objects.filter(payment_reservation=self)
            total_sell_price = 0
            total_payment_price = 0
            total_cost_price = 0
            for e in all_lines: ### add if agencia
                try:
                    sp = PriceProduct.objects.filter(lineXprice=e)

                    try:
                        lr = e.lineXrate
                        perc = lr.percentage
                    except:
                        perc = 0

                    intermediate_sell_price = sp[0].net - (sp[0].net * sp[0].percent_discount / 100)  #### have to add a total payment price somewhere
                    total_sell_price += intermediate_sell_price - intermediate_sell_price*perc/100
                    print('sell price added to total')
                except:
                    print('No sell price for line'+str(e))
                total_cost_price += e.cost_price
            for f in all_prices:
                total_payment_price += f.price

            # Update of payment and to pay
            self.total_payments = total_payment_price
            self.total_to_pay = total_sell_price
            self.total_costs = total_cost_price
            if total_sell_price == total_payment_price:
                self.payment_state = 'P'
                print('changed reservation to paid')

                #return '[AUTOMATIC SAVE]'
            else:
                self.payment_state = 'W'
                print('changed reservation to waiting for payment')
                #return ''
            #self.save()

    PAYMENT_STATE = [
        ('P', 'PAID'),
        ('W', 'WAITING FOR PAYMENT'),
        ('SB', 'STANDBY'),
    ]

    number_reservation = models.AutoField(primary_key=True) # Auto incrementation, unique
    payment_state = models.TextField(choices=PAYMENT_STATE, default='W') ###has to be a readonly if sum payments is = to total
    more_info = models.TextField(default='',blank=True,null=True)
    total_payments = models.IntegerField(null=True)
    total_to_pay = models.IntegerField(null=True)
    total_costs = models.IntegerField(null=True)
    ### KEYS
    user = models.ForeignKey( ### OR GET ALL LOGGED IN USERS? solamente persona de atec, el guia va a ser en las lignas
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            null=True
        )

    def get_cname(self):
        class_name = 'Reservation'
        return class_name

    def __str__(self):
        return str(self.number_reservation)


class PaymentReservation(General):  ###created only when a client has paid
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    date = models.DateTimeField(default=timezone.now)

    ### KEYS
    type_payment = models.ForeignKey(
        TypePayment,
        on_delete=models.PROTECT,
        null=True
    )
    payment_reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        null=True
    )

    def get_cname(self):
        class_name = 'PaymentReservation'
        return class_name

    def updt_payment_state(self, this_reservation, *args, **kwargs): ### if a paymentstate is on stand by we will not do anything
        if this_reservation.payment_state != 'SB':
            all_lines = LineReservation.objects.filter(line_reservation=this_reservation)
            all_prices = PaymentReservation.objects.filter(payment_reservation=this_reservation)
            total_sell_price = 0
            total_payment_price = 0
            total_cost_price = 0
            for e in all_lines:
                try:
                    sp = PriceProduct.objects.filter(lineXprice=e)

                    try:
                        lr = e.lineXrate
                        perc = lr.percentage

                    except:
                        perc = 0

                    intermediate_sell_price = sp[0].net - (sp[0].net * sp[0].percent_discount / 100)  #### have to add a total payment price somewhere
                    total_sell_price += intermediate_sell_price - intermediate_sell_price*perc/100
                    print('sell price added to total')
                except:
                    print('No sell price for line'+str(e))
                total_cost_price += e.cost_price
            for f in all_prices:
                total_payment_price += f.price

            # Update of payment and to pay
            this_reservation.total_payments = total_payment_price
            this_reservation.total_to_pay = total_sell_price
            this_reservation.total_costs = total_cost_price
            # Update of payment state
            if total_sell_price == total_payment_price:

                this_reservation.payment_state = 'P'
                print('changed reservation to paid')

                #return '[AUTOMATIC SAVE]'
            else:
                this_reservation.payment_state = 'W'
                print('changed reservation to waiting for payment')
                #return ''
            this_reservation.save(update_fields=['payment_state','total_costs','total_to_pay','total_payments'])


    def __str__(self):
        return str(self.price)+' '+str(self.date)


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
        return str(self.percentage)+' '+str(self.year)

class LineReservation(General):
    PAYMENT_CHOICES = [
        ('P','PAID'),
        ('NP', 'NOT PAID'),
    ]

    quantity = models.IntegerField(default=1,validators=[MinValueValidator(0)])
    date_start = models.DateField(null=True,blank=True)
    date_end = models.DateField(default=timezone.now)
    cost_price = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    payment_guide = models.TextField(choices = PAYMENT_CHOICES, default='NP')
    # sell_price = models.IntegerField(default=0,validators=[MinValueValidator(0)])

    ###KEYS
    client = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name='clientXperson',
        null=True
    )
    line_reservation = models.ForeignKey( #CHANGE THE NAME
        Reservation,
        on_delete=models.CASCADE,
        related_name='lineXreservation'
    )

    guide = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name='lineXguide',
        null=True
    )
    sell_price = models.ForeignKey(
        PriceProduct,
        on_delete=models.CASCADE,
        related_name='lineXprice'
    )
    line_product = models.ForeignKey( #change the name AND SELECT THE PRODUCTS OF THE GUIDE ONLY
        Product,
        on_delete=models.PROTECT,
        related_name='lineXproduct',
        null=True
    )
    line_rate = models.ForeignKey(
        Rate,
        on_delete=models.PROTECT,
        related_name='lineXrate',
        null=True
    )
    line_tax = models.ForeignKey( ###modifier ultérieurement avec vérification de la date actuelle
        Tax,
        on_delete=models.PROTECT,
        related_name='lineXtax',
        null=True
    )

    def __str__(self):
        return 'Line Reservation number ' +str(self.id)

    def get_cname(self):
        class_name = 'LineReservation'
        return class_name

    def updt_payment_state(self, this_reservation, *args, **kwargs): ### (doubled the function to be able to use self.thisfunction in general where we cant import those classes (circular import) if a paymentstate is on stand by we will not do anything
        if this_reservation.payment_state != 'SB':
            all_lines = LineReservation.objects.filter(line_reservation=this_reservation)
            all_prices = PaymentReservation.objects.filter(payment_reservation=this_reservation)
            total_sell_price = 0
            total_payment_price = 0
            total_cost_price = 0
            for e in all_lines: ### add if agencia
                try:
                    sp = PriceProduct.objects.filter(lineXprice=e)

                    try:
                        lr = e.lineXrate
                        perc = lr.percentage
                    except:
                        perc = 0

                    intermediate_sell_price = sp[0].net - (sp[0].net * sp[0].percent_discount / 100)  #### have to add a total payment price somewhere
                    total_sell_price += intermediate_sell_price - intermediate_sell_price*perc/100
                    print('sell price added to total')
                except:
                    print('No sell price for line'+str(e))
                total_cost_price += e.cost_price
            for f in all_prices:
                total_payment_price += f.price

            # Update of payment and to pay
            this_reservation.total_payments = total_payment_price
            this_reservation.total_to_pay = total_sell_price
            this_reservation.total_costs = total_cost_price

            if total_sell_price == total_payment_price:
                this_reservation.payment_state = 'P'
                print('changed reservation to paid')

                #return '[AUTOMATIC SAVE]'
            else:
                this_reservation.payment_state = 'W'
                print('changed reservation to waiting for payment')
                #return ''
            this_reservation.save(update_fields=['payment_state', 'total_costs', 'total_to_pay', 'total_payments'])

            #this_reservation.save()

