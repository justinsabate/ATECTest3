from django.shortcuts import render, get_object_or_404
from .models import Servicio


def print_servicio(request):
    servicios = Servicio.objects.all()
    return render(request,'app/print_servicio.html',{'servicios':servicios})

def servicio_detail(request,pk):
    detail = get_object_or_404(Servicio, pk=pk)
    return render(request, 'app/servicio_detail.html', {'detail': detail})