from django.urls import path
from . import views

urlpatterns=[
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name="checkout"),
    path('login/',views.login_page,name='login'),
    path('register/',views.register,name='register'),
    path('product/<str:pk>/', views.product_page,name='product'),
    path('payment/',views.process_payment,name='process-payment'),
    path('payment-done/', views.payment_done, name = 'payment-done'),
    path('payment_cancelled/',views.payment_cancelled,name='payment-cancelled'),
]