from django.db.models.deletion import CASCADE
from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Product(models.Model):
    customers=models.ManyToManyField(User,blank=True)
    name = models.CharField(max_length=200, unique=True)
    # size = models.CharField(max_length=7, default="EU 00")
    # product_code=models
    price = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)
    order=models.IntegerField(default=1,null=False)
    rating=models.IntegerField(default=5)
    country_of_origin=models.CharField(max_length=50, default="Nigeria", null=True)
    description=models.TextField(null=True,blank=True)
    colour = models.CharField(default='N/A', max_length=15)
    avatar = models.ImageField(null=True, default="cart.jpg")
    total = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)
    updated=models.DateTimeField(auto_now=True) #will take a time stamp when the model is updated
    created=models.DateTimeField(auto_now_add=True) #auto_now_add only takes the first time. It does not update
   
    def __str__(self):
        return self.name

#class Quantity(models.Model):
#    quantity=models.IntegerField(default=1,null=True)
    

    

