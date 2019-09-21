from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


from .product_classes import PriceProduct
from .person_classes import Person
from .general import General
from django.conf import settings

class TypePayment(General):
    type = models.CharField(max_length=100, default='CASH')

    def get_cname(self):
        class_name = 'TypePayment'
        return class_name

class Reservation(General):



    PAYMENT_STATE = [
        ('P', 'PAID'),
        ('W', 'WAITING FOR PAYMENT'),
        ('SB', 'STANDBY'),
    ]

    number_reservation = models.AutoField(primary_key=True) # Auto incrementation, unique
    payment_state = models.TextField(choices=PAYMENT_STATE, default='W') ###has to be a readonly if sum payments is = to total
    more_info = models.TextField(default='',blank=True,null=True)

    ### KEYS
    client = models.ManyToManyField(Person, related_name='clientXperson') # attention limit choices has to be changed if typeperson is added/modified
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            null=True
        )

    def get_cname(self):
        class_name = 'Reservation'
        return class_name


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

    def updt_payment_state(self, this_reservation): ### if a paymentstate is on stand by we will not do anything
        if this_reservation.payment_state != 'SB':
            all_lines = LineReservation.objects.filter(line_reservation=this_reservation)
            all_prices = PaymentReservation.objects.filter(payment_reservation=this_reservation)
            total_sell_price = 0
            total_payment_price = 0
            for e in all_lines:
                total_sell_price += e.sell_price
            for f in all_prices:
                total_payment_price += f.price
            if total_sell_price == total_payment_price:
                this_reservation.payment_state = 'P'
                print('changed reservation to paid')
                this_reservation.save()
                #return '[AUTOMATIC SAVE]'
            else:
                this_reservation.payment_state = 'W'
                print('changed reservation to waiting for payment')
                #return ''

class LineReservation(General):
    quantity = models.IntegerField(default=0)
    date_start = models.DateField(null=True,blank=True)
    date_end = models.DateField(default=timezone.now)
    cost_price = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    sell_price = models.IntegerField(default=0,validators=[MinValueValidator(0)])

    ###KEYS
    line_reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='lineXreservation'
    )
    price = models.ForeignKey(
        PriceProduct,
        on_delete=models.CASCADE,
        related_name='lineXprice'
    )
    guide = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name='lineXguia'
    )

    def get_cname(self):
        class_name = 'LineReservation'
        return class_name

    def updt_payment_state(self, this_reservation): ### (doubled the function to be able to use self.thisfunction in general where we cant import those classes (circular import) if a paymentstate is on stand by we will not do anything
        if this_reservation.payment_state != 'SB':
            all_lines = LineReservation.objects.filter(line_reservation=this_reservation)
            all_prices = PaymentReservation.objects.filter(payment_reservation=this_reservation)
            total_sell_price = 0
            total_payment_price = 0
            for e in all_lines:
                total_sell_price += e.sell_price
            for f in all_prices:
                total_payment_price += f.price
            if total_sell_price == total_payment_price:
                this_reservation.payment_state = 'P'
                print('changed reservation to paid')
                this_reservation.save()
                #return '[AUTOMATIC SAVE]'
            else:
                this_reservation.payment_state = 'W'
                print('changed reservation to waiting for payment')
                #return ''
