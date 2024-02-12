from django.shortcuts import get_object_or_404
from .models import Order, Coupon

def apply_coupon_to_order(order_id, coupon_code):
    order = get_object_or_404(Order, order_id=order_id)
    coupon = get_object_or_404(Coupon, code=coupon_code)
    order.applied_coupon = coupon
    order.save()