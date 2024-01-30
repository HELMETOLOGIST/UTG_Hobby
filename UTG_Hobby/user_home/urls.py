from django.urls import path
from . import views


urlpatterns = [
    path('',views.homee,name='home'),
    path('contact/',views.contactt,name='contact'),
    path('about/',views.aboutt,name='about'),
    path('custom_404/',views.custom_404,name='custom_404'),
    
    
]