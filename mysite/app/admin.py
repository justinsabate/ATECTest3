from django.contrib import admin
from .models import Client
from .models import Reservation


def link(modeladmin, request, queryset):
    queryset.update(client=2)
link.short_description = "link client 0 to the selected reservation"



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name','fam_name','tarifa')
    ordering = ('name',)
    search_fields = ('name','fam_name','tarifa')

# @admin.register(Reservation)
# class ClientAdmin(admin.ModelAdmin):
#     list_display = ('numero','client')
#     ordering = ('numero',)
#     search_fields = ('numero','client')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('numero',)
    ordering = ('numero',)
    search_fields = ('numero',)
    actions = [link]


#admin.site.register(ReservationAdmin)
#admin.site.register(Reservation)