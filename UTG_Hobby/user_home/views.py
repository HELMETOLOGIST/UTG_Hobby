from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from user_authentication.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user_products.models import Brands,Category,ColorVarient,Products,Image
from django.views.decorators.cache import cache_control
from admin_side.models import Banner
from django.core.paginator import Paginator
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homee(request):
    variants = ColorVarient.objects.filter(is_listed=True,product__is_listed=True).order_by('-id')
    banner = Banner.objects.filter(is_listed=True)
    context = {
        'homeVariant': variants,
        'banner': banner,
    }
    return render(request, 'home.html', context)



def contactt(request):
    return render(request, 'contact.html')

def aboutt(request):
    return render(request, 'about.html')