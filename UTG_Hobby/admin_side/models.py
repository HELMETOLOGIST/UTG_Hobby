from django.db import models
from user_products.models import ColorVarient

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=500)
    image = models.ImageField(upload_to='banner')
    variant = models.ForeignKey(ColorVarient, on_delete=models.CASCADE, null=True)
    is_listed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title