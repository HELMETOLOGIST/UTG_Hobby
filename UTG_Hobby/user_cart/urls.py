from django.urls import path
from . import views

urlpatterns = [
    path('cart/',views.cartt,name='cart'),
    path('addcart/',views.addcartt,name='addcart'),
    path('remove_item_from_cart/',views.remove_item_from_cartt,name='remove_item_from_cart'),
    path('update_cart/', views.update_cartt, name='update_cart'),
    path('checkout/', views.checkoutt, name='checkout'),
    path('add_address_checkout/',views.add_address_checkoutt,name='add_address_checkout'),
    path('edit_addresss/<str:id>',views.edit_addressss,name='edit_addresss'),
    path('delete_address/<str:id>',views.delete_addresss,name='delete_addresss'),
    

]
