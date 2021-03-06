from django.contrib import admin
from mysite.app.models_OLD import Client
from mysite.app.models_OLD import Reservation
from mysite.app.models_OLD import Tarea
from mysite.app.models_OLD import Servicio


def link(modeladmin, request, queryset):
    queryset.update(client=3)
    #cli = Client.object.filter(id=queryset.get(modeladmin.client))
    #cli.res=queryset.numero
link.short_description = "link client 0 to the selected reservation"

class ReservationInline(admin.TabularInline): #nous permet d'afficher les réservations dans les clients
    model = Reservation.client.through

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name','fam_name','tarifa')
    ordering = ('name',)
    search_fields = ('name','fam_name','tarifa')
    inlines = [
        ReservationInline, #nous permet d'afficher les réservations dans les clients
    ]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('numero',)
    ordering = ('numero',)
    search_fields = ('numero',)
    #actions = [link]

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('description','estado','staff')
    ordering = ('estado',)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display=('Nombre',)
    list_display = ('Nombre',)


#admin.site.register(ReservationAdmin)
#admin.site.register(Reservation)