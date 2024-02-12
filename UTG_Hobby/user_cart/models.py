from django.db import models
from user_authentication.models import *
from user_products.models import *


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(ColorVarient, on_delete=models.CASCADE)
    prod_quantity = models.IntegerField(null=False, blank=False, default=1)
    cart_price = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.product.product.products_name
    
    
   

# Create your models here.
