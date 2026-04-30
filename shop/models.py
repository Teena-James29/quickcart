from django.db import models

# Create your models here.
from django.contrib.auth.models import User



class category(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=30)
    price=models.IntegerField()
    desc=models.TextField()
    img1=models.ImageField(upload_to='Product',null=True,blank=True)
    img2=models.ImageField(upload_to='Product',null=True,blank=True)
    img3=models.ImageField(upload_to='Product',null=True,blank=True)
    ctry=models.ForeignKey(category,on_delete=models.CASCADE,null=True,blank=True)
    us=models.ForeignKey(User,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.name
    

class Profile(models.Model):
    image = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    phone=models.CharField(max_length=10)
    us=models.OneToOneField(User,on_delete=models.CASCADE)
     
    def __str__(self):
         return str(self.us)
    



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField()

    def __str__(self):
        return f"Order {self.id} - {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.product.price * self.quantity