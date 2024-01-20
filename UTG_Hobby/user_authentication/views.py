
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
import random
from user_authentication.forms import OtpForm 
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from allauth.socialaccount.models import SocialAccount
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def loginn(request):
    if 'email' in request.session:
        return redirect('home')
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request,user)
            return redirect("home")
        else:
            messages.error(request, "Username or Password incorrect")
            return redirect(loginn)  
    else:
        return render(request, 'login.html')
    

@csrf_exempt
def logoutt(request):
    auth_logout(request)
    return redirect("login")




def signupp(request):
    if 'email' in request.session:
        return redirect('home')
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        
            first_name = request.POST.get("first_name")
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            elif CustomUser.objects.filter(phone_number=phone).exists():
                messages.error(request, "Phone Number already exists.")
            elif len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long")
            elif password != confirm_password:
                messages.error(request, "Passwords do not match")
            else:
                nums = '1234567890'
                otp = ''.join(random.choice(nums) for _ in range(6))
                request.session["otp"] = otp
                

                user = CustomUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone,
                    password=password,
                    username=email,
                    otp=otp
                )

                subject = 'OTP Verification Code'
                message = otp
                template_path = 'email_otp.html'
                html_message = render_to_string(template_path, {'first_name': first_name, 'email_otp': otp})
                send_mail(subject,message,settings.DEFAULT_FROM_EMAIL, [user.email],html_message=html_message, fail_silently=False)
                request.session["email_otp"] = email
                return redirect('otp')
            
    return render(request, 'signup.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otpp(request):
    email = request.session.get('email_otp')
    user = CustomUser.objects.get(email=email)
    
    
    if request.method == 'POST':
        otp = request.POST['otp']
        session_otp = request.session.get('otp', None)
        if otp == session_otp:
            user.is_listed = True
            del request.session['otp']
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP")
            return redirect('otp')
    return render(request,'otp.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def resend_otpp(request):
    email = request.session.get('email_otp')
    user = CustomUser.objects.get(email=email)
    new_otp = ''.join(random.choice('1234567890') for _ in range(6))
    request.session['otp'] = new_otp
    subject = 'New OTP Verification Code'
    message = new_otp
    user.otp = new_otp
    user.save()
    first_name = user.first_name
    template_path = 'email_otp.html'
    html_message = render_to_string(template_path, {'first_name': first_name, 'email_otp': new_otp})
    send_mail(subject,message,settings.DEFAULT_FROM_EMAIL, [user.email],html_message=html_message, fail_silently=False)
    return redirect("otp")

        


    

