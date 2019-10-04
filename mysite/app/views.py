from django.shortcuts import render, get_object_or_404
from .models.reservation_classes import Reservation,LineReservation,PriceProduct,AgeDiscount
from .models.general import ATEC,COUPON
from django.http import HttpResponse
from django.views.generic import View
from .models.reservation_classes import Person,LanguagePerson
import math
# importing get_template from loader
from django.template.loader import get_template

# import render_to_pdf from util.py
from .utils import render_to_pdf


# Creating PDF
class GeneratePdf(View):
    def get(self, request,number_reservation,id_client,coupon, *args, **kwargs):
        # getting the template
        reservation = get_object_or_404(Reservation, number_reservation=number_reservation)
        atec = ATEC.objects.all()

        atec_0=atec[0]


        if id_client!=0: ### if we want the receipt for the whole resrevation
            client = get_object_or_404(Person,id=id_client)
            lines = LineReservation.objects.filter(line_reservation=reservation,client=client)
            try :
                line = lines[0]
                total_to_pay = reservation.get_total_to_pay_CLIENT(lines)
            except:
                print('no line in reservation')
                total_to_pay=0

            if coupon != 0:
                coup = COUPON.objects.get(numero=coupon)
                pdf = render_to_pdf('pdf_client.html',{'reservation': reservation, 'lines': lines,'ATEC':atec_0,'client':client,'line':line,'total_to_pay':total_to_pay,'coupon':coup})
            else: ### we do not give the information to HTML so it cant put the image
                pdf = render_to_pdf('pdf_client.html',
                                    {'reservation': reservation, 'lines': lines, 'ATEC': atec_0, 'client': client,
                                     'line': line, 'total_to_pay': total_to_pay})


        else :
            lines = LineReservation.objects.filter(line_reservation=reservation)
            total_to_pay=reservation.get_total_to_pay_RESERVATION()
            if coupon != 0:
                coup = COUPON.objects.get(numero=coupon)
                pdf = render_to_pdf('pdf_reservation.html',{'reservation': reservation, 'lines': lines,'ATEC':atec_0,'total_to_pay':total_to_pay,'coupon':coup})
            else:
                pdf = render_to_pdf('pdf_reservation.html', {'reservation': reservation, 'lines': lines, 'ATEC': atec_0,
                                                             'total_to_pay': total_to_pay})

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

# Test, create the HTML page before creating the PDF
def before_PDF(request,number_reservation):
    reservation = get_object_or_404(Reservation, number_reservation=number_reservation)
    lines = LineReservation.objects.filter(line_reservation=reservation)
    atec = ATEC.objects.all()

    return render(request,'app/pdf_test.html', {'reservation': reservation, 'lines': lines,'ATEC':atec[0]})


