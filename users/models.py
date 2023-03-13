from django.db import models
from django.contrib.auth.models import AbstractUser
from bit68.models import Product
# Create your models here.

class User(AbstractUser):

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username =  models.CharField(max_length=255, default="")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']


class CartItem(models.Model):
    
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.user.username) + " " + str(self.product.product_name)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(CartItem)
    total_price = models.FloatField(default=0)


    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)
         
class OrderItem(models.Model):
    
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.user.username) + " " + str(self.product.product_name)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    total_price = models.FloatField(default=0)


    def get_order_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)
         
