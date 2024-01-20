from django.urls import path
from . import views


urlpatterns = [
    path('shop/',views.shops,name='shop'),
    path('products_details/<str:id>/',views.products_detailss,name='products_details'),
]