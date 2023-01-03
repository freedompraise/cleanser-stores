#DJANGO
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponseRedirect , reverse
#APP
from .forms import RegistrationForm, LoginForm
from .models import Product
#PAYPAL
from paypal.standard.forms import PayPalPaymentsForm

import random


# Create your views here.

def store(request):
    all = Product.objects.all()
    context={'all':all}
    return render(request,'store/store.html',context)

# @login_required(login_url='login')
def product_page(request,pk):
    product=Product.objects.get(id=pk)
    discount=str(0.83*float(product.price))
    save=str(0.17*float(product.price))
    if request.method=='POST':
        if request.user.is_authenticated:
            product.customers.add(request.user)
            product.order=request.POST.get('quantity') if request.POST.get('qauntity') else product.order
            product.save()
            return redirect('cart')
        else:
            return redirect('login')

    context={"product":product,'discount':discount[:4],'save':save[:4]}
    return render(request,'store/product.html',context)

@login_required(login_url='login')
def checkout(request):
    user=request.user
    products = user.product_set.all()
    total_dict={}
    discount_dict={}
    count=int()

    for item in products:
        item.order=request.POST.get(item.name) if request.POST.get(item.name) else item.order
        item.save


    for product in products:
        if product.order is not None:
            product.total= int(product.order) * int(product.price)
            product.discount = float(str(0.13 * float(product.total))[:4])
            product.save()
            total_dict[product.id]=product.total
            discount_dict[product.id]=product.discount
            count+=1

    if request.POST.get("delete")=='delete':
        product.customers.remove(request.user)
        product.save()

    total_int=int()
    for value in total_dict.values():
        total_int+=value
        
    discount=str(0.13*float(total_int))
    discount=discount.split('.')

    context={"products":products, "total":total_int,'discount':discount[0]+'.'+discount[1][:2],'count':count}
    return render(request,'store/checkout.html',context)


@login_required(login_url='login')
def cart(request):
    user=request.user
    products = user.product_set.all()
    total_dict={}
    discount_dict={}
    
    # assigning a quantity for each item in the cart page
    for item in products:
        item.order=request.POST.get(item.name) if request.POST.get(item.name) else item.order
        item.save

    # calculating for total in all products by multiplying their price with quantity
    for product in products:
        if product.order is not None:
            product.total= int(product.order) * int(product.price)
            product.discount = float(str(0.13 * float(product.total))[:4])
            product.save()
            total_dict[product.id]=product.total
            discount_dict[product.id]=product.discount

    total_int=int()
    for value in total_dict.values():
        total_int+=value
        
    discount=str(0.13*float(total_int))
    discount=discount.split('.')

    if request.POST.get("delete")=='delete':
        product.customers.remove(request.user)
        product.save()

    context={"products":products, "total":total_int,'discount':discount[0]+'.'+discount[1][:2]}
    return render(request,'store/cart.html',context) 


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Welcome back! You are now logged in.')
                return redirect(request.META.get('HTTP_REFERER','store'))
            else:
                messages.error(request,'Invalid Login credentials')
                return redirect('login')
        else:  
            form =  LoginForm()
            
    return render(request,'store/login.html',{'form':LoginForm})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(request.META.get('store', reverse('store')))
            form.save()
            auth_login(request,user)
    else:
        form = RegistrationForm()
    return render(request,'store/register.html', {'form':form})

    # PAYPAL
    



def process_payment(request):
    products = cart.products
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(cart.total_int),
        'item_name': str([product.name+'\n' for product in products]),
      #  'invoice': str([product.name+'\n' for product in Product.objects.all()])
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment-done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment-cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'store/payment.html', {'order': products, 'form': form,'page':'process'})


@csrf_exempt
def payment_done(request):
    return render(request, 'store/payment.html',{'page':'done'})

@csrf_exempt
def payment_cancelled(request):
    return render(request, 'store/payment.html',{'page':'cancelled'})