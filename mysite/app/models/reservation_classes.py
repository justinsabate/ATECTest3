from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


from .product_classes import Product,Tax
from .person_classes import Person
from .general import General,get_all_logged_in_users,Action
from django.conf import settings


import datetime
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
        on_delete=models.SET_NULL
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
                    sp = PriceProduct.objects.filter(lineXprice=e) ##this one is unique

                    ### For Children reduction
                    try:
                        agedisc = sp.agediscount
                        age_percentage = agedisc.percentage
                    except:
                        age_percentage = 0
                    print('Age percentage '+str(age_percentage))
                    intermediate_sell_price = sp[0].rack - (sp[0].rack * age_percentage / 100)

                    ### For agency reduction
                    try:
                        ratedisc = RateDiscount.objects.filter(ratediscount=sp[0])
                        rate_percentage = ratedisc[0].percentage
                    except:
                        rate_percentage = 0
                    print('Rate percentage ' + str(rate_percentage))
                    intermediate_sell_price = intermediate_sell_price - (intermediate_sell_price * rate_percentage / 100)

                    ### For special offer reduction
                    try:
                        print('Special offer percentage ' + str(specialoffer_percent_discount))
                    except:
                        specialoffer_percent_discount = 0
                        print('Special offer percentage ' + str(rate_percentage))
                    intermediate_sell_price = intermediate_sell_price - (intermediate_sell_price * specialoffer_percent_discount / 100)

                    ### Quantity multiplication
                    intermediate_sell_price = intermediate_sell_price*e.quantity
                    ### Add calculated total to line
                    e.discounted = intermediate_sell_price
                    super(General, e).save(*args, **kwargs)  ###TOADD
                    ### Add if to total
                    total_sell_price += intermediate_sell_price
                    print('sell price added to total')


                except:
                    print('No sell price for line'+str(e))
                #total_cost_price += e.cost_price
            for f in all_prices:
                total_payment_price += f.price

            # Update of payment and to pay
            self.total_payments = total_payment_price
            self.sub_total_to_pay = total_sell_price #subtotal without tax

            ### Tax payment
            this_tax = Tax.objects.filter(reservationXtax=self)
            self.total_to_pay = total_sell_price*(1+(this_tax[0].percentage/100))

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
                    sp = PriceProduct.objects.filter(lineXprice=e) ##this one is unique

                    ### For Children reduction
                    try:
                        agedisc = sp.agediscount
                        age_percentage = agedisc.percentage
                    except:
                        age_percentage = 0
                    print('Age percentage '+str(age_percentage))
                    intermediate_sell_price = sp[0].rack - (sp[0].rack * age_percentage / 100)

                    ### For agency reduction
                    try:
                        ratedisc = RateDiscount.objects.filter(ratediscount=sp[0])
                        rate_percentage = ratedisc[0].percentage
                    except:
                        rate_percentage = 0
                    print('Rate percentage ' + str(rate_percentage))
                    intermediate_sell_price = intermediate_sell_price - (intermediate_sell_price * rate_percentage / 100)

                    ### For special offer reduction
                    try:
                        print('Special offer percentage ' + str(specialoffer_percent_discount))
                    except:
                        specialoffer_percent_discount = 0
                        print('Special offer percentage ' + str(rate_percentage))
                    intermediate_sell_price = intermediate_sell_price - (intermediate_sell_price * specialoffer_percent_discount / 100)

                    ### Quantity multiplication
                    intermediate_sell_price = intermediate_sell_price*e.quantity
                    ### Add calculated total to line
                    e.discounted = intermediate_sell_price
                    super(General, e).save(*args, **kwargs)  ###TOADD
                    ### Add if to total
                    total_sell_price += intermediate_sell_price
                    print('sell price added to total')


                except:
                    print('No sell price for line'+str(e))
                #total_cost_price += e.cost_price
            for f in all_prices:
                total_payment_price += f.price

            # Update of payment and to pay
            this_reservation.total_payments = total_payment_price
            this_reservation.sub_total_to_pay = total_sell_price #subtotal without tax

            ### Tax payment
            this_tax = Tax.objects.filter(reservationXtax=this_reservation)
            this_reservation.total_to_pay = total_sell_price*(1+(this_tax[0].percentage/100))

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
    date_start = models.DateField(null=True,blank=True)
    date_end = models.DateField(default=timezone.now)
    #cost_price = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    payment_guide = models.TextField(choices = PAYMENT_CHOICES, default='NP')
    # sell_price = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    discounted =  models.FloatField(null=True,blank=True,default=0, validators=[MinValueValidator(0.0)])
    ###KEYS
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
                    sp = PriceProduct.objects.filter(lineXprice=e) ##this one is unique
                    try:
                        #agedisc = sp.agediscount
                        agedisc = AgeDiscount.objects.filter(agediscount=sp[0])
                        age_percentage = agedisc[0].percentage
                    except:
                        age_percentage = 0
                        print('error agedisc')
                    print('Age percentage '+str(age_percentage))
                    intermediate_sell_price = sp[0].rack - (sp[0].rack * age_percentage / 100)

                    ### For agency reduction
                    try:
                        #ratedisc = sp.ratediscount
                        ratedisc = RateDiscount.objects.filter(ratediscount=sp[0])
                        rate_percentage = ratedisc[0].percentage
                    except:
                        rate_percentage = 0
                    print('Rate percentage ' + str(rate_percentage))
                    intermediate_sell_price = intermediate_sell_price - (intermediate_sell_price * rate_percentage / 100)

                    ### For special offer reduction
                    try:
                        print('Special offer percentage ' + str(specialoffer_percent_discount))
                    except:
                        specialoffer_percent_discount = 0
                        print('Special offer percentage ' + str(rate_percentage))
                    intermediate_sell_price = intermediate_sell_price - (intermediate_sell_price * specialoffer_percent_discount / 100)

                    ### Quantity multiplication
                    intermediate_sell_price = intermediate_sell_price*e.quantity
                    ### Add calculated total to line
                    e.discounted = intermediate_sell_price

                    super(General, e).save(*args, **kwargs) ###TOADD

                    ### Add if to total
                    total_sell_price += intermediate_sell_price
                    print('sell price added to total')


                except:
                    print('No sell price for line'+str(e))
                #total_cost_price += e.cost_price
            for f in all_prices:
                total_payment_price += f.price

            # Update of payment and to pay
            this_reservation.total_payments = total_payment_price
            this_reservation.sub_total_to_pay = total_sell_price #subtotal without tax

            ### Tax payment
            this_tax = Tax.objects.filter(reservationXtax=this_reservation)
            this_reservation.total_to_pay = total_sell_price*(1+(this_tax[0].percentage/100))

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



    # FORMER
    # def updt_payment_state(self, this_reservation, *args, **kwargs): ### (doubled the function to be able to use self.thisfunction in general where we cant import those classes (circular import) if a paymentstate is on stand by we will not do anything
    #     if this_reservation.payment_state != 'SB':
    #         all_lines = LineReservation.objects.filter(line_reservation=this_reservation)
    #         all_prices = PaymentReservation.objects.filter(payment_reservation=this_reservation)
    #         total_sell_price = 0
    #         total_payment_price = 0
    #         total_cost_price = 0
    #         for e in all_lines: ### add if agencia
    #             try:
    #                 sp = PriceProduct.objects.filter(lineXprice=e)
    #
    #                 try:
    #                     lr = e.lineXrate
    #                     perc = lr.percentage
    #                 except:
    #                     perc = 0
    #
    #                 intermediate_sell_price = sp[0].net - (sp[0].net * sp[0].percent_discount / 100)  #### have to add a total payment price somewhere
    #                 total_sell_price += intermediate_sell_price - intermediate_sell_price*perc/100
    #                 print('sell price added to total')
    #             except:
    #                 print('No sell price for line'+str(e))
    #             total_cost_price += e.cost_price
    #         for f in all_prices:
    #             total_payment_price += f.price
    #
    #         # Update of payment and to pay
    #         this_reservation.total_payments = total_payment_price
    #         this_reservation.total_to_pay = total_sell_price
    #         this_reservation.total_costs = total_cost_price
    #
    #         if total_sell_price == total_payment_price:
    #             this_reservation.payment_state = 'P'
    #             print('changed reservation to paid')
    #
    #             #return '[AUTOMATIC SAVE]'
    #         else:
    #             this_reservation.payment_state = 'W'
    #             print('changed reservation to waiting for payment')
    #             #return ''
    #         this_reservation.save(update_fields=['payment_state', 'total_costs', 'total_to_pay', 'total_payments'])
    #
    #         #this_reservation.save()

