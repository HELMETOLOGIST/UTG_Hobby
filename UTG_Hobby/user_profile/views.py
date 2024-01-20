from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from user_authentication.models import CustomUser
from django.contrib.auth.decorators import login_required
from .models import *
from user_order.models import *
import re
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout

# Create your views here.

# @login_required
# def user_profilee(request):
#     email = request.user.email
#     user = get_object_or_404(CustomUser, email=email)
#     user_data = Address.objects.filter(user=user, is_present=True)
#     order = Order.objects.filter(user=user)
#     print(order)
#     order_item = OrderItem.objects.all()
#     print(order_item)
#     return render(request, 'user_profile.html', {"user":user, "address_data":user_data, "order_item":order_item})
    
    
@login_required
def user_profilee(request):
    email = request.user.email
    user = get_object_or_404(CustomUser, email=email)
    user_data = Address.objects.filter(user=user, is_present=True)
    orders = Order.objects.filter(user=user).exclude(order_id__exact='')
    order_items = OrderItem.objects.all()

    return render(request, 'user_profile.html', {"user": user, "address_data": user_data, "order_item": order_items, "orders": orders})
    

@login_required
def update_profilee(request):
    email = request.user
    user = get_object_or_404(CustomUser, email=email)
    
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phno = request.POST.get('phno')
        
        user.first_name = fname
        user.last_name = lname
        user.phone_number = phno
        user.save()

        # Return a JSON response
        return JsonResponse({'message': 'Profile updated successfully'})

    context = {'user': user}
    return render(request, 'user_profile.html', context)


@login_required
def change_passwordd(request):
    if request.method == "POST":
        user = request.user
        current_password = request.POST.get('currentpass')
        new_password = request.POST.get('newpass')
        confirm_password = request.POST.get('confirmpass')

        if check_password(current_password, user.password):
            if new_password == confirm_password:               
                user.set_password(new_password)
                user.save()
                logout(request)
                return JsonResponse({'message': 'Password changed successfully'}, status=200)
            else:
                messages.error(request, 'Password and Confirm Password do not match!')
        else:
            messages.error(request, 'Current Password is incorrect!')

    return JsonResponse({'message': 'Failed to change password'}, status=400)

@login_required
def add_address_userr1(request):
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
        
        return redirect('user_profile')
    return render(request, 'add_address_checkout.html')

@login_required
def edit_address_userr1(request,id):
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
        
        return redirect('user_profile')
    return render(request, 'edit_address_user.html',{'address':address})
    
@never_cache
def delete_address_userr1(request,id):
    addres = get_object_or_404(Address, id=id)
    addres.is_present=False
    addres.save()
    return JsonResponse({'status':"Deleted Successfully"})