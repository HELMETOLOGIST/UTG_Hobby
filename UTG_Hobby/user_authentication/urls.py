from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('login/',views.loginn,name='login'),
    path('signup/',views.signupp,name='signup'),
    path('otp/',views.otpp,name='otp'),
    path('logout/',views.logoutt,name='logout'),
    path('resend_otp/',views.resend_otpp, name='resend_otp'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),
]
