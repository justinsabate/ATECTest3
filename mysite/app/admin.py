from django.contrib import admin
from . import models
from .forms import RequiredInlineFormSet


#### USEFUL THINGS ####

### IMPORTS ###
# from mysite.app.models_OLD import Client

### TO CREATE AN ACTION ###
# def link(modeladmin, request, queryset):
#     queryset.update(client=3)
#     #cli = Client.object.filter(id=queryset.get(modeladmin.client))
#     #cli.res=queryset.numero
# link.short_description = "link client 0 to the selected reservation"

# @admin.register(Reservation)
# class ReservationAdmin(admin.ModelAdmin):
#     actions = [link]

### TO PRINT AN INFORMATION (here manytomany) IN ANOTHER CLASS
# class ReservationInline(admin.TabularInline): #nous permet d'afficher les réservations dans les clients
#     model = Reservation.client.through
#
# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     inlines = [
#         ReservationInline, #nous permet d'afficher les réservations dans les clients
#     ]

# ### TO ORDER AND SEARCH ###
# @admin.register(Tarea)
# class TareaAdmin(admin.ModelAdmin):
#     list_display = ('description','estado','staff')
#     ordering = ('estado',)
#     search_fields = ('name', 'fam_name', 'tarifa')
import os
from .models.product_classes import Product,AttributeProduct,Location,PriceProduct,ImageProduct,StockProduct, Rate
from .models.general import General,Action,Task,get_all_logged_in_users
from .models.person_classes import LanguagePerson,Person,Mail,Phone,TypePerson
from .models.reservation_classes import TypePayment, PaymentReservation, Reservation,LineReservation,Tax
# class Type_ProductInline(admin.TabularInline): #nous permet d'afficher les réservations dans les clients
#     model = Product.type.through

#admin.site.register(State)
import shutil
from django.db.models.signals import pre_delete
from django.dispatch import receiver


# @receiver(pre_delete)
# def delete_repo(sender, instance, **kwargs):
#     ### Get the user
#     users = get_all_logged_in_users()
#     user = ''
#     for e in users:
#         user += str(e)
#
#
#     ### Create the action
#     try:
#         classes = instance.get_cname()
#     except:
#         print('we are trying to delete a non model object, maybe the session is closing') #for example the Sessin
#     else:
#         if classes != 'General' and classes != 'Action': #because each time we delete an object we delete the general object linked to it
#             s = str(instance.last_modification) + ' ' + user + ' deleted element ' + str(
#                 instance.id) + ' of class ' + instance.get_cname()
#             print(s)
#             Action.objects.create(act=s)

### GENERAL.PY ###
class GeneralAdmin(admin.ModelAdmin):
    readonly_fields = ('creation', 'last_modification','id')

@admin.register(Action)
class ActionAdmin(GeneralAdmin):
    readonly_fields = ('action','creation', 'last_modification','id','act','state')

@admin.register(Task)
class TaskAdmin(GeneralAdmin):
    users = get_all_logged_in_users()
    user = ''
    for e in users: ###hope that is only one user logger
        if e.is_superuser :
            readonly_fields = ('creation', 'last_modification', 'assigner_auto')
    #if User.objects.filter(is_superuser=True):
        else :
            readonly_fields = (
            'assigned_date',
            'description',
            'assigned_user',
            'assigner_auto',
            'creation',
            'state',
            'last_modification',
            'delivery_date',
            'cause')
    list_display = ('task_state', 'assigned_date', 'description', 'assigned_user','assigner_auto')
    ordering = ('task_state', )

### PRODUCT_CLASSES.PY ###

@admin.register(AttributeProduct)
class AttributeProduct(GeneralAdmin):
    list_display = ('text',)

@admin.register(Location)
class Location(GeneralAdmin):
    list_display = ('address',)

@admin.register(PriceProduct)
class PriceProduct(GeneralAdmin):
    list_display = ('year','percent_discount','information','date_start_offer','date_end_offer')

class PriceInLine(admin.StackedInline):
    model = models.PriceProduct
    fk_name = 'price_product'
    extra = 0
    readonly_fields = ('creation', 'last_modification',)
    formset = RequiredInlineFormSet #to set a required foreign key


@admin.register(StockProduct)
class StockProduct(GeneralAdmin):
    list_display = ('nb_stock','nb_shop')

@admin.register(ImageProduct)
class ImageProduct(GeneralAdmin):
    list_display = ('short_title',)

@admin.register(Rate)
class RateAdmin(GeneralAdmin):
    list_display = ('text','percentage')

@admin.register(Product) ###Nous permet d'hériter des fields readonly de generaladmin
class ProductAdmin(GeneralAdmin):
    list_display = ('type','name','description',)
    inlines = [
        PriceInLine,
    ]

### PERSON_CLASSES.PY ###

@admin.register(LanguagePerson)
class LanguagePerson(GeneralAdmin):
    list_display = ('lang',)

@admin.register(TypePerson)
class TypePersonAdmin(GeneralAdmin):
    list_display = ('type',)

@admin.register(Mail)
class MailAdmin(GeneralAdmin):
    list_display = ('email','per')

class MailInline(admin.StackedInline):
    model = models.Mail
    fk_name = 'per'
    extra = 1
    readonly_fields = ('creation', 'last_modification',)
    formset = RequiredInlineFormSet #to set a required foreign key

@admin.register(Phone)
class PhoneAdmin(GeneralAdmin):
    list_display = ('tel','per')

class PhoneInline(admin.StackedInline):
    model = models.Phone
    fk_name = 'per'
    extra = 1
    readonly_fields = ('creation', 'last_modification',)
    formset = RequiredInlineFormSet


@admin.register(Person)
class PersonAdmin(GeneralAdmin):
    list_display = ('type','name','NIN','nationality')
    inlines = [
        MailInline,
        PhoneInline,
    ]

### RESERVATION_CLASSES ###

@admin.register(TypePayment)
class TypePaymentReservationAdmin(GeneralAdmin):
    list_display = ('type',)

@admin.register(PaymentReservation)
class PaymentReservationAdmin(GeneralAdmin):
    list_display = ('type_payment','date','payment_reservation')

class PaymentReservationInLine(admin.StackedInline):
    model = models.PaymentReservation
    fk_name = 'payment_reservation'
    extra = 0
    readonly_fields = ('creation', 'last_modification',)

@admin.register(LineReservation)
class LineReservationAdmin(GeneralAdmin):
    list_display = ('line_reservation','cost_price','sell_price',)

class LineReservationInLine(admin.StackedInline):
    model = models.LineReservation
    fk_name = 'line_reservation'
    extra = 0
    readonly_fields = ('creation', 'last_modification',)

@admin.register(Reservation)
class ReservationAdmin(GeneralAdmin):
    list_display = ('number_reservation','payment_state')
    readonly_fields = ('number_reservation','total_payments','total_to_pay','total_costs','payment_state','creation', 'last_modification',)
    inlines = [
        LineReservationInLine,
        PaymentReservationInLine,
    ]

@admin.register(Tax)
class TaxAdmin(GeneralAdmin):
    list_display = ('year','percentage','text')

