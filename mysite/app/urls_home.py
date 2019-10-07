
from django.urls import path, include
from django.views.generic.base import TemplateView # new

urlpatterns = [
    path('', TemplateView.as_view(template_name='app/home/home.html'), name='home'), # new
]
