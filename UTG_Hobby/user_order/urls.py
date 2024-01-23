from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_orderr,name='place_order'),
    path('order_succes/',views.order_success,name="order_succes"),
    path('order_details/<str:order_id>/',views.order_detailss,name='order_details'),
    path('cancel_order/<str:id>/',views.cancel_orderr,name='cancel_order'),
    path('return_order/',views.return_orderr,name='return_order'),
    path('invoice',views.invoice,name='invoice'),
    path('user_invoice/<str:order_id>/',views.user_invoicee,name='user_invoice'),
    path('apply_coupons/', views.apply_coupons, name='apply_coupons'),
    # path('remove_coupon/', views.remove_coupon, name='remove_coupon'),

]
