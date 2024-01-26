from django.db import models
from user_authentication.models import CustomUser
from user_products.models import ColorVarient
# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    variant = models.ForeignKey(ColorVarient, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rating = models.IntegerField()
    
    def __str__(self):
        return self.user.first_name
    
        