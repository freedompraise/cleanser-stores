from django.urls import path
from .views import product

urlpatterns=[
    path('products/', product, name ="products")
]