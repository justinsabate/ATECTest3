from django.urls import path
from . import views
from .views import GeneratePdf

import os

# urlpatterns = [
#     path('', views.print_servicio, name='print_servicio'),
#     path('servicio/<int:pk>/', views.servicio_detail, name='servicio_detail'),
# ]

### for pdf generation
from django.conf.urls import url
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
    path('app/<int:number_reservation>/', views.before_PDF, name='before_PDF'),
    #path('app/pdf/<int:number_reservation>/download', views.index, name='before_index'),
    path('reservation-<int:number_reservation>/client-<int:id_client>/coupon-<int:coupon>/pdf/', GeneratePdf.as_view()),
 ]

#url(r'^pdf/$',
