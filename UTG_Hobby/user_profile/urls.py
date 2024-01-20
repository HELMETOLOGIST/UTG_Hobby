from django.urls import path
from . import views

urlpatterns = [
    path('user_profile',views.user_profilee,name='user_profile'),
    path('update_profile/',views.update_profilee,name='update_profile'),
    path('change_password/',views.change_passwordd,name='change_password'),
    path('add_address_user/',views.add_address_userr1,name='add_address_user'),
    path('edit_address_user/<str:id>',views.edit_address_userr1,name="edit_address_user"),
    path('delete_address_user/<str:id>/',views.delete_address_userr1,name="delete_address_user"),
    

]
