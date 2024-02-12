from django.utils import timezone
import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from user_products.models import Brands, Category, Products, Image,ColorVarient
from user_authentication.models import CustomUser
from user_cart.models import Cart
from django.http import JsonResponse, HttpResponse
from user_profile.models import Address
from user_coupon.models import Coupon,CouponUsage
# Create your views here.

@login_required
def cartt(request):
    user = request.user
    cart_item = Cart.objects.filter(user=user).order_by('id')
    subPrice = cart_item.values_list("cart_price", flat=True)
    total = sum(subPrice)
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
    context = {
        "cart_items":cart_item,
        "total":total,
    }
    return render(request, 'cart.html', context)


@login_required
def addcartt(request):
    if request.method == 'POST':
        user = request.user
        prod_id = int(request.POST.get("product_id"))
        prod_check = ColorVarient.objects.get(id=prod_id)
        
        if Cart.objects.filter(user=user, product=prod_check):
            return JsonResponse({"status":"Product already in cart"})
        else:
            prod_q = 1
            if prod_check.quantity >= prod_q:
                product = get_object_or_404(ColorVarient, id=prod_id)
                Cart.objects.create(
                    user=user,
                    product=product,
                    prod_quantity=prod_q,
                    cart_price=product.discounted_price(),
                )
                cart_count = Cart.objects.filter(user=user).count()
                return JsonResponse(
                    {
                        "status":"Product added successfully",
                        "success":True,
                        "cart_count":cart_count
                    }
                )
            else:
                return JsonResponse(
                    {
                        "status":f"Only {(prod_check.quantity)} Quantity avialable"
                    }
                )
    else:
        return redirect('login')
    
        
@login_required
def remove_item_from_cartt(request):
    if request.method == "POST":
        user = request.user
        item_id = request.POST.get("item_id")
        try:
            cart_item = get_object_or_404(Cart, id=item_id, user=user)
            cart_item.delete()
            return JsonResponse({"message":"Item removed successfully"})
        except Cart.DoesNotExist:
            return JsonResponse({"message":"Item not found"}, status=400)
    else:
        return JsonResponse({"message":"Invalid request method"}, status=405)


@login_required
def update_cartt(request):
    if request.method == "POST":
        email = request.user.email
        user = CustomUser.objects.filter(email=email).first()
        change = int(request.POST.get("change"))
        variant_id = request.POST.get("variantId")
        varient_obj = get_object_or_404(ColorVarient, id=variant_id)

        cart = get_object_or_404(Cart, user=user, product=varient_obj)

        if change == 1:
            if varient_obj.quantity > cart.prod_quantity:
                cart.prod_quantity += 1
                cart.save()

        else:
            if cart.prod_quantity > 1:
                cart.prod_quantity -= 1
                cart.save()
            else:
                cart.prod_quantity = 1
                cart.save()

        priceOfInstance = varient_obj.discounted_price()
        prodtotal = cart.prod_quantity * priceOfInstance
        cart.cart_price = prodtotal
        cart.save()
        cart_items = Cart.objects.filter(user=user)
        total = sum(cart_items.values_list("cart_price", flat=True))
        
    response_data = {
        "updatedQuantity": cart.prod_quantity,
        "prodtotal": prodtotal,
        "total": total,
        "variant_cont":varient_obj.quantity ,
    }
    return JsonResponse(response_data)


from django.db.models import Sum

@login_required
def checkoutt(request):
    email = request.user.email
    user = get_object_or_404(CustomUser, email=email)
    address = Address.objects.filter(user=user, is_present=True)
    cart_items = Cart.objects.filter(user=user)
    cart_count = cart_items.count()
    total_cart_price = sum(cart_items.values_list("cart_price", flat=True))
    coupons = Coupon.objects.filter(is_active=True, exp_date__gte=timezone.now())
    
    # Retrieve total coupon amount used by the user
    total_coupon_amount = CouponUsage.objects.filter(user=user).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Calculate the total amount after deducting coupon amount
    total_amount = total_cart_price - total_coupon_amount
    request.session['total_amount'] = total_amount
    context = {
        "addresses": address,
        "cart_items": cart_items,
        'total_cart_price': total_cart_price,
        'total_coupon_amount': total_coupon_amount,
        'total_amount': total_amount,
        'cart_count': cart_count,
        'coupons': coupons,
    }
    
    return render(request, "checkout.html", context)




@login_required
def add_address_checkoutt(request):
    email = request.user.email
    user = get_object_or_404(CustomUser, email=email)
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        new_address = Address(
            user=user,
            name=name,
            phone=phone,
            street_address=street_address,
            city=city,
            state=state,
            pin_code=pincode,
        )
        new_address.save()
        
        return redirect('checkout')
        
    return render(request, 'add_address_checkout.html')


def edit_addressss(request,id):
    address = get_object_or_404(Address, id=id)
    
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        address.name = name
        address.phone = phone
        address.street_address = street_address
        address.city = city
        address.state = state
        address.pin_code = pincode
        address.save()
        return redirect('checkout')
    return render(request, 'edit_address.html',{'address':address})


def delete_addresss(request, id):
    add = get_object_or_404(Address, id=id)
    add.is_present=False
    add.save()
    return JsonResponse({'status':"Deleted Successfully"})