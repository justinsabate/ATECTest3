from django.contrib import admin
from .models import Client
from .models import Reservation


admin.site.register(Client)
admin.site.register(Reservation)