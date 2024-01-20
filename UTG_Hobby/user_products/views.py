from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from user_authentication.models import CustomUser
from django.contrib import messages
from user_products.models import Brands, Category, Products, Image,ColorVarient

# Create your views here.

def shops(request):
    selected_categories = request.GET.getlist('selected_categories')
    selected_brands = request.GET.getlist('selected_brands')
    print(selected_categories)
    print(selected_brands)

    variants = ColorVarient.objects.filter(is_listed=True, product__is_listed=True)

    if selected_categories:
        variants = variants.filter(product__category_id__id__in=selected_categories)

    if selected_brands:
        variants = variants.filter(product__brand_id__id__in=selected_brands)

    Cat_list = Category.objects.filter(is_listed=True)
    Bran_list = Brands.objects.filter(is_listed=True)
    print(Cat_list)
    print(Bran_list)

    context = {
        'variants': variants.order_by('-id'),  # Ensure ordering is applied here
        "Cat_list": Cat_list,
        "Bran_list": Bran_list,
    }

    return render(request, 'shop.html', context)


def products_detailss(request, id):
    variants = ColorVarient.objects.filter(id=id).first()
    context = {
        "product" : variants
    }
    return render(request, 'products_details.html', context)



