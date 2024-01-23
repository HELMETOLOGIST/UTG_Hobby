from django.db import models
from user_authentication.models import CustomUser
# Create your models here.

class Coupon(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    exp_date = models.DateField()
    usage_limit = models.PositiveIntegerField(default=1)
    user_count = models.PositiveIntegerField(default=0)
    is_active =models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, related_name="usage", null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="usage", null=True)
    total_amount = models.PositiveIntegerField(null=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    

    
    
    