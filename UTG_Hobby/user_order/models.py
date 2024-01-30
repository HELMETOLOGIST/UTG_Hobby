from django.db import models
from user_authentication.models import *
from user_products.models import *
from user_cart.models import *
from user_profile.models import *
from user_products.models import *
import uuid
from user_coupon.models import *
# Create your models here.

class Order(models.Model):
    order_id = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=150, null=False)
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    expected_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, null=False, decimal_places=2)
    applied_coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    applied_offer = models.ForeignKey(ColorVarient, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    def generate_order_id(self):
        return str(uuid.uuid4().hex)[:8]
  


    def __str__(self):
        return f"{self.user.first_name}'s Order | ID : {self.order_id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    variant = models.ForeignKey(ColorVarient, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    modified_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=150, default='Pending')
    
    def __str__(self) -> str:
        return '{} - {} - {}'.format(self.order.user.first_name,self.id, self.order.order_id)
    
    