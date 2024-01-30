from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from user_authentication.models import CustomUser
from django.contrib import messages
from user_products.models import Brands, Category, Products, Image,ColorVarient
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from user_review.models import Review
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def shops(request):
    selected_categories = request.GET.getlist('selected_categories')
    selected_brands = request.GET.getlist('selected_brands')
    
    request.session['selected_categories'] = selected_categories
    request.session['selected_brands'] = selected_brands
    
    search = request.GET.get('search')
    if search:
        variants = ColorVarient.objects.filter(is_listed=True, product__is_listed=True, product__products_name__icontains=search).order_by('-id')
    else:
        variants = ColorVarient.objects.filter(is_listed=True, product__is_listed=True).order_by('-id')

    if selected_categories:
        variants = variants.filter(product__category_id__in=selected_categories)

    if selected_brands:
        variants = variants.filter(product__brand_id__in=selected_brands)

    Cat_list = Category.objects.filter(is_listed=True)
    Bran_list = Brands.objects.filter(is_listed=True)

    # Pagination
    paginator = Paginator(variants, 9)  # Show 10 variants per page
    page = request.GET.get('page')

    try:
        variants = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        variants = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        variants = paginator.page(paginator.num_pages)

    context = {
        'variants': variants,
        'Cat_list': Cat_list,
        'Bran_list': Bran_list,
    }

    return render(request, 'shop.html', context)



def products_detailss(request, id):
    print(id)
    email = request.user
    print(email)
    variants = ColorVarient.objects.filter(id=id).first()
    print(variants)
    
    if request.method == "POST":
        star_rating = request.POST.get('rating')
        item_review = request.POST.get('message')
        
        # Check if star_rating is a valid number
        if star_rating and star_rating.isdigit():
            # Convert star_rating to an integer
            star_rating = int(star_rating)
        else:
            # Handle the case where star_rating is not a valid number
            star_rating = None
        
        review = Review(
            user=email,
            variant=variants,
            review=item_review,
            rating=star_rating,
        )
        review.save()
        
        # Redirect to the same page to avoid form resubmission
        return redirect('products_details', id=id)

    all_rev = Review.objects.filter(variant=variants)
        
    context = {
        "product": variants,
        'review_rating': all_rev,   
    }
    return render(request, 'products_details.html', context)







