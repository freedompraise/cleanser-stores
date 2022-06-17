from django.db.models.deletion import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# class User(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     is_active = models.BooleanField(default=True)
#     staff = models.BooleanField(default=False) # a admin user; non super-user
#     admin = models.BooleanField(default=False) # a superuser

#     # notice the absence of a "Password field", that is built in.

#     # USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = [] # Email & Password are required by default.

#     def get_full_name(self):
#         # The user is identified by their email address
#         return self.email

#     def get_short_name(self):
#         # The user is identified by their email address
#         return self.email

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         return self.staff

#     @property
#     def is_admin(self):
#         "Is the user a admin member?"
#         return self.admin



# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_staffuser(self, email, password):
#         """
#         Creates and saves a staff user with the given email and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password):
#         """
#         Creates and saves a superuser with the given email and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.admin = True
#         user.save(using=self._db)
#         return user

# # hook in the New Manager to our Model
# class User(AbstractBaseUser): # from step 2
#     ...
#     objects = UserManager()







class Product(models.Model):
    customer=models.ManyToManyField(User,blank=True)
    name = models.CharField(max_length=200)
    # size = models.CharField(max_length=7, default="EU 00")
    # product_code=models
    price = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)
    order=models.IntegerField(default=1,null=False)
    rating=models.IntegerField(default=5)
    country_of_origin=models.CharField(max_length=50, default="Nigeria", null=True)
    description=models.TextField(null=True,blank=True)
    total=models.IntegerField(default=1)
    #colour = ColorField(default='#FF0000')
    avatar = models.ImageField(null=True, default="image.jpg")
    updated=models.DateTimeField(auto_now=True) #will take a time stamp when the model is updated
    created=models.DateTimeField(auto_now_add=True) #auto_now_add only takes the first time. It does not update
   
    def __str__(self):
        return self.name

#class Quantity(models.Model):
#    quantity=models.IntegerField(default=1,null=True)
    

    

