from django.urls import path
from . import views


urlpatterns = [
    path('wallet',views.wallett,name='wallet'),
    path('add_to_wallet',views.add_to_wallett,name='add_to_wallet'),
    path('update_wallet',views.update_wallett,name='update_wallet'),
]
