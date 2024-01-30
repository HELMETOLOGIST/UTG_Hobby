from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Brands(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Products(models.Model):
    products_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE,)
    brand_id = models.ForeignKey(Brands,on_delete=models.CASCADE)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.products_name
    
class ColorVarient(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='colorvarient_set')
    color = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()
    is_listed = models.BooleanField(default=True)
    product_offer = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def discounted_price(self):
        discount_percentage = self.product_offer
        if discount_percentage > 0:
            return self.price - ((self.price * discount_percentage) / 100)
        else:
            return self.price

    def __str__(self):
        return f"{self.product.products_name} - {self.color}"
    
    
    
class Image(models.Model):
    variant = models.ForeignKey(ColorVarient,on_delete=models.CASCADE,null = True, related_name='images')
    image = models.ImageField(upload_to="product_images")
    
