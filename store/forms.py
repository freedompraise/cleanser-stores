from django.forms import ModelForm,forms
from .models import Product
from django.contrib.auth.models import User

class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields='__all__'

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['email','password','username']
    