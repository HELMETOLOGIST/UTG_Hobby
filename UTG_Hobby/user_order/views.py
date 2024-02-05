from decouple import config
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from user_products.models import Brands, Category, Products, Image,ColorVarient
from user_authentication.models import CustomUser
from user_cart.models import Cart
from django.http import JsonResponse, HttpResponse
from user_profile.models import Address
from django.db import transaction
import json
from django.views.decorators.cache import never_cache
from django.db.models import Sum
import uuid
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib import messages
from user_order.models import Order, OrderItem
import razorpay
from user_wallet.models import Wallet
from django.conf import settings
from decimal import Decimal, ROUND_DOWN
from user_coupon.models import Coupon,CouponUsage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Value, DecimalField

def order_success(request):
    if request.user.is_authenticated:
        order_id = request.session.get('order_id')

        if order_id:
            order = get_object_or_404(Order, order_id=order_id)
            order_items = OrderItem.objects.filter(order=order)

            # Update the queryset to order by discounted_price in reverse order
            order_items = order_items.annotate(
                discounted_price=F('variant__discounted_price')
            ).order_by('-discounted_price')

            context = {
                "order": order,
                "order_items": order_items,
            }
            return render(request, 'confirmation.html', context)
        else:
            messages.error(request, 'Invalid or missing order ID in session.')
            return redirect('home')  # Redirect to home or another appropriate page


client = razorpay.Client(auth=(config('RAZORPAY_API_KEY'), config('RAZORPAY_API_SECRET_KEY')))

# Create your views here.

@login_required
@never_cache
def place_orderr(request):
    if request.user.is_authenticated:
        email = request.user.email
        print(email)
        user = get_object_or_404(CustomUser, email=email)
        cart_items = Cart.objects.filter(user=user)
        out_of_stock_items = [item for item in cart_items if item.prod_quantity > item.product.quantity]
        if out_of_stock_items:
            return JsonResponse({'empty': True,  'message': 'Some cart items are out of stock'})
        
        if request.method == "POST":
            address_id = request.POST.get('addreselect')
            payment_mode = request.POST.get('payment_mode')
            cart_items = Cart.objects.filter(user=user)
            coupon_disc = CouponUsage.objects.filter(user=user)
            delivery_address = get_object_or_404(Address, user=user, id=address_id)
            coupon_code = request.POST.get('coupon_code')
            
            if payment_mode == 'cod':
                if cart_items.exists():
                    try:
                        with transaction.atomic():
                            total_price = 0
                            if 'final_amount' in request.session:
                                final_amount = int(request.session['final_amount'])
                            else:
                                total_price = sum(cart_items.values_list("cart_price", flat=True))

                            print("price:",total_price)
                            order = Order.objects.create(
                                user = user,
                                address = delivery_address,
                                payment_mode = payment_mode,
                                quantity = 0,
                                total_price = final_amount if 'final_amount' in request.session else total_price,
                            )
                            
                            for cart_item in cart_items:
                                order_item = OrderItem.objects.create(
                                    order = order,
                                    variant = cart_item.product,
                                    price = cart_item.cart_price,
                                    quantity = cart_item.prod_quantity,
                                    status = "Order Confirmed",
                                    
                                )
                                
                                products = cart_item.product
                                products.quantity -= cart_item.prod_quantity
                                products.save()
                                
                                order.quantity += order_item.quantity
                                cart_item.delete()
                                
                            order.expected_date = (order.order_date + timedelta(days=7))
                            order.save()
                            request.session['order_id'] = str(order.order_id)
                            
                            response_data = {
                                'success': True,
                                'message': 'Your order has been placed successfully',
                                'order_id': order.order_id,
                            }
                            return JsonResponse(response_data)
                    except Exception as e:
                        print('Error occured while placing the order : ',e)
                        response_data = {
                            'success': False,
                            'message': 'An error occurred while processing your order'
                        }
                        return JsonResponse(response_data)
                else:
                    response_data = {
                        'success': False,
                        'message': 'Your Cart is empty.'
                    }
                    return JsonResponse(response_data)
                
                # razorpay integration code here
            if payment_mode == 'razor':
                if cart_items.exists():
                    try:
                        with transaction.atomic():
                            total_price = 0
                            if 'final_amount' in request.session:
                                final_amount = int(request.session['final_amount'])
                                print('final:',final_amount)
                            else:
                                total_price = sum(cart_items.values_list("cart_price", flat=True))
                                print('total:',total_price)

                            # Create Order instance
                            order = Order.objects.create(
                                user=user,
                                address=delivery_address,
                                payment_mode=payment_mode,
                                quantity=0,
                                total_price = final_amount if 'final_amount' in request.session else total_price
                            )

                            # Create OrderItem instances
                            for cart_item in cart_items:
                                order_item = OrderItem.objects.create(
                                    order=order,
                                    variant=cart_item.product,
                                    price=cart_item.cart_price,
                                    quantity=cart_item.prod_quantity,
                                    status="Order Confirmed",
                                )
                                
                                products = cart_item.product
                                products.quantity -= cart_item.prod_quantity
                                products.save()
                                
                                order.quantity += order_item.quantity
                                cart_item.delete()
                            
                            order.expected_date = (order.order_date + timedelta(days=7))
                            order.save()
                            request.session['order_id'] = str(order.order_id)
                            total_price = final_amount if 'final_amount' in request.session else total_price,
                            # Create Razorpay order
                            
                            razorpay_order_data = {
                                'amount': total_price * 100,  # Amount in paise
                                'currency': 'INR',
                                'receipt': str(order.order_id),
                            }
                            
                            response_data = {
                                'success': True,
                                'message': 'Your order has been placed successfully',
                            }
                            return JsonResponse(response_data)

                    except Exception as e:
                        print('Error occurred while placing the order. Exception Type:', type(e).__name__)
                        print('Exception Value:', str(e))
                        response_data = {
                            'success': False,
                            'message': 'An error occurred while processing your order'
                        }
                        return JsonResponse(response_data)

                          
                else:
                    response_data = {
                        'success': False,
                        'message': 'Your Cart is empty.'
                    }
                    return JsonResponse(response_data)
                
            if payment_mode == 'wallet':
                cart_items = Cart.objects.filter(user=user)
                if cart_items.exists():
                    try:
                        with transaction.atomic():
                            total_price = 0
                            if 'final_amount' in request.session:
                                final_amount = int(request.session['final_amount'])
                            else:
                                total_price = sum(cart_items.values_list("cart_price", flat=True))
                            user_wallet = Wallet.objects.filter(user=user).last()
                            last = user_wallet.balance_amount
                            print(last)
                        
                            if user_wallet.balance_amount >= total_price:
                                order = Order.objects.create(
                                    user=user,
                                    address=delivery_address,
                                    payment_mode=payment_mode,
                                    quantity=0,
                                    total_price = final_amount if 'final_amount' in request.session else total_price,
                                )
                                
                                for cart_item in cart_items:
                                    order_item = OrderItem.objects.create(
                                        order=order,
                                        variant=cart_item.product,
                                        price=cart_item.cart_price,
                                        quantity=cart_item.prod_quantity,
                                        status="Order Confirmed",
                                    )
                                    
                                    products = cart_item.product
                                    products.quantity -= cart_item.prod_quantity
                                    products.save()
                                
                                    order.quantity += order_item.quantity
                                    cart_item.delete()
                                
                                order.expected_date = (order.order_date + timedelta(days=7))
                                order.save()
                                request.session['order_id'] = str(order.order_id)
                                
                                amount = request.session["amount"]
                                total_price = final_amount if 'final_amount' in request.session else total_price
                                new = last - total_price
                                new = Decimal(new)
                                wallet_s = Wallet(
                                    user=user,
                                    balance_amount=new,
                                    transaction_type="Debit",
                                    transaction_details=f'Purchased for Rs.{total_price}.00',
                                    date=timezone.now(),
                                    transaction_amount=amount,
                                )
                                wallet_s.save()
                                
                                response_data = {
                                    'success':True,
                                    "message":"Your order has been placed successfully.",
                                    'order_id':order.order_id,
                                    'insufficient_balance':False,
                                }
                            else:
                                response_data = {
                                    'success': False,
                                    'message':'Insufficient Balance in your wallet.',
                                    'insufficient_balance': True,
                                }
                            return JsonResponse(response_data)
                    except Exception as e:
                        response_data = {
                            'success':False,
                            'message':'Error while placing order',
                        }
                        return JsonResponse(response_data)
                    
                else:
                    response_data = {
                        'success':False,
                        'message':'Your cart is empty',
                    }
                    return JsonResponse(response_data)      
    else:
        response_data = {
        'success': False,
        'message': 'Please Login to place an Order!'
        }
        return JsonResponse(response_data)
        

def order_success(request):
    if request.user.is_authenticated:
        order_id = request.session.get('order_id')
        
        
        if order_id:
            order = get_object_or_404(Order, order_id=order_id)
            order_items = OrderItem.objects.filter(order=order)
            total_discounted_price = sum(item.variant.discounted_price() for item in order_items)
            print(total_discounted_price)
            
            context = {
                "order": order,
                "order_items": order_items,
                'total_discounted_price':total_discounted_price,
            }
            return render(request, 'confirmation.html', context)
        else:
            messages.error(request, 'Invalid or missing order ID in session.')
            return redirect('home')  # Redirect to home or another appropriate page
      

def cancel_orderr(request,id):
    email = request.user.email
    user = get_object_or_404(CustomUser, email=email)
    order = get_object_or_404(OrderItem, id=id)
    order.status = "Cancelled"
    if order.order.payment_mode == "COD":
        order.variant.quantity += order.quantity
        order.save()
        order.variant.save()
        return redirect('order_details', order_id=order.order_id) 
    else:
        order.variant.quantity += order.quantity
        amount = order.price * order.quantity
        user_wallet = Wallet.objects.filter(user=user).order_by("-id").first()
        
        if not user_wallet:  # Check if wallet is None
            balance_amount = 0
        else:
            balance_amount = user_wallet.balance_amount

        balance = balance_amount + Decimal(amount)
        Wallet.objects.create(
            user=user,
            balance_amount=balance,
            transaction_type="Credit",
            transaction_details=f"Recieved Money through Order Cancel",
            transaction_amount=amount,
        )
        order.save()
        order.variant.save()
        messages.error(request,'product already delivered ')  
        return redirect('order_details', order_id=order.order.order_id)    


def return_orderr(request):
    email = request.session["email"]
    user = get_object_or_404(CustomUser, email=email)
    order = get_object_or_404(OrderItem, id=id)
    order.status = "Returned"
    
    order.variant.quantity += order.quantity
    amount = order.price * order.quantity
    user_wallet = Wallet.objects.filter(user=user).order_by("-id").first()
        
    if not user_wallet:  # Check if wallet is None
        balance_amount = 0
    else:
        balance_amount = user_wallet.balance_amount

    balance = balance_amount + Decimal(amount)
    Wallet.objects.create(
        user=user,
        balance_amount=balance,
        transaction_type="Credit",
        transaction_details=f"Recieved Money through Refund",
        transaction_amount=amount,
    )
    order.save()
    order.variant.save()
    messages.error(request,'product already delivered ')  
    return redirect('order_details')
    
    
@login_required
def order_detailss(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        total_discounted_price = sum(item.variant.discounted_price() for item in order_items)
        print(total_discounted_price)        
        product_ids = [item.variant.product.id for item in order_items]
        print(order_items)
        context = {
            "order": order,
            "order_items": order_items,
            "product_ids": product_ids,
            "total_discounted_price":total_discounted_price,
        }

        return render(request, 'order.html', context)
    else:
        return HttpResponse("Unauthorized", status=401)
    

def invoice(request):
    if request.user.is_authenticated:
        order_id = request.session.get('order_id')
        coupon_id = request.session.get('coupon_id')
        if coupon_id:
            coupon = get_object_or_404(Coupon, id=coupon_id)
        
        if order_id:
            order = get_object_or_404(Order, order_id=order_id)
            order_items = OrderItem.objects.filter(order=order)
            context = {
                "order": order,
                "order_items": order_items,
                "coupon": coupon if coupon_id else None,
                
            }
            
            return render(request, 'invoice.html', context)
        else:
            messages.error(request, 'Invalid or missing order ID in session.')
            return redirect('home')  # Redirect to home or another appropriate page
        
@login_required
def user_invoicee(request,order_id):
    if request.user.is_authenticated:
        coupon_id = request.session.get('coupon_id')
        order = get_object_or_404(Order, order_id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        total_discounted_price = sum(item.variant.discounted_price() for item in order_items)
        if coupon_id:
            coupon = get_object_or_404(Coupon, id=coupon_id)
        
        product_ids = [item.variant.product.id for item in order_items]
        print(order_items)
        context = {
            "order": order,
            "order_items": order_items,
            "product_ids": product_ids,
            "coupon": coupon if coupon_id else None,
            "total_discounted_price":total_discounted_price,
        }

        return render(request, 'user_invoice.html', context)
    else:
        return HttpResponse("Unauthorized", status=401)
    
    
@login_required
def apply_coupons(request):
    """
    This function will handle coupons
    
    """
    if request.method == "POST":
        email = request.user.email
        user = get_object_or_404(CustomUser, email=email)
        
        coupon_code = request.POST.get('couponCode', '')
        coupon_check = Coupon.objects.filter(code=coupon_code, is_active=True).first()

        if coupon_check:
            if CouponUsage.objects.filter(user=user, coupon=coupon_check).exists():
                return JsonResponse({'error': 'Coupon Already Applied'})

            if coupon_check.user_count < coupon_check.usage_limit:
                cart_total = sum(Cart.objects.filter(user=user).values_list("cart_price", flat=True))
                if cart_total >= coupon_check.minimum_purchase:
                    if coupon_check.exp_date < timezone.now().date():
                        return JsonResponse({'error': 'Coupon Expired'})
                    
                    total = cart_total - coupon_check.discount_price
                    request.session['final_amount'] = int(total)
                    
                    response_data = {
                        'success': 'Apply Successfully',
                        'total': total,
                        'coupon_code': coupon_code,
                        'discount_amount': coupon_check.discount_price,
                    }
                    
                    coupon_check.user_count += 1
                    coupon_check.save()
                    
                    # Store coupon ID in session
                    request.session['coupon_id'] = coupon_check.id

                    CouponUsage.objects.create(user=user, coupon=coupon_check)
                    return JsonResponse(response_data)
                else:
                    return JsonResponse(
                        {"error": f"Minimum Purchase Amount {round(coupon_check.minimum_purchase)} Required"}
                    )
            else:
                return JsonResponse({'error': "This code reached its usage limit."})
        else:
            return JsonResponse({"error": "Invalid Coupon."})
              
    return JsonResponse({'error': 'Invalid Request.'})




# @login_required
# def remove_coupon(request):
#     email = request.user.email
#     user = get_object_or_404(CustomUser, email=email)
    
#     coupon_code = request.POST.get('couponCode', '')
#     coupon_check = Coupon.objects.filter(code=coupon_code, is_active=True).first()
    
#     if coupon_check:
#         usage_check = CouponUsage.objects.filter(user=user, coupon=coupon_check).first()
#         if usage_check:
#             coupon_check.user_count -= 1
#             coupon_check.save()
#             usage_check.delete()
        
#         # Remove coupon ID from session
#         if 'coupon_id' in request.session:
#             del request.session['coupon_id']

#     total = sum(Cart.objects.filter(user=user).values_list("cart_price", flat=True))
    
#     response_data = {
#         "total": total,
#         "success": "removed"
#     }
#     return JsonResponse(response_data)

    