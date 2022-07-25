from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import random


# Create your views here.
def get_total(products):
    total_dict={}
    for product in products:
        if product.order is not None:
            product.total= int(product.order) * int(product.price)
            product.discount = float(str(0.13 * float(product.total))[:4])
            product.save()
            total_dict[product.id]=product.total
    total_int=int()
    for value in total_dict.values():
        total_int+=value
    return total_int


def store(request):
    all = Product.objects.all()
    context={'all':all}
    return render(request,'store/store.html',context)

def product_page(request,pk):
    product=Product.objects.get(id=pk)
    # products = request.user.product_set.all() if request.user.is_authenticated else ''
    discount=str(0.83*float(product.price))
    save=str(0.17*float(product.price))
    if request.method=='POST':
        if request.user.is_authenticated:
            product.customers.add(request.user)
            product.order=request.POST.get('quantity') if request.POST.get('quantity') else product.order
            product.save()
            return redirect('cart')
        else:
            return redirect('login')

    context={"product":product,'discount':discount[:4],'save':save[:4]}
    return render(request,'store/product.html',context)

@login_required(login_url='login')
def checkout(request):
    products = request.user.product_set.all()
    # calculating for total in all products by multiplying their price with quantity
    total_int = get_total(products)
    discount=str(0.13*float(total_int))
    discount=discount.split('.')
    count=products.count()
    context={"products":products, "total":total_int,'discount':discount[0]+'.'+discount[1][:2],'count':count}
    return render(request,'store/checkout.html',context)


@login_required(login_url='login')
def cart(request):
    products = request.user.product_set.all()
    # assigning a quantity for each item in the cart page
    for item in products:
        item.order=request.POST.get(item.name) if request.POST.get(item.name) else item.order
        if request.POST.get(str(item.id)) == 'delete':
            # HOW TO IDENTIFY THE DELETE
            item.customers.remove(request.user)
        item.save()

    # calculating for total in all products by multiplying their price with quantity
    total_int = get_total(products)
    discount=str(0.13*float(total_int))
    discount=discount.split('.')

    context={"products":products, "total":total_int,'discount':discount[0]+'.'+discount[1][:2]}
    return render(request,'store/cart.html',context) 


def login_page(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
        user=User.objects.get(email=email)
        if user is not None:
            auth_login(request, user)
            return redirect('store')
    except:  
        messages.error(request,'Username or Password not correct')
            
    return render(request,'store/login.html')



def register(request):
    user=User.objects.create(
    username=request.POST.get('username'),
    email=request.POST.get('email'),
    password=request.POST.get('email')
    )
    if user is not None:
        auth_login(request, user)
        return redirect('store')
    else:
        return messages.error(request, "error occurred in registration")
    context={'form':form}
    return render(request,'store/register.html')

    # PAYPAL
    
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

def process_payment(request):
    products = request.user.product_set.all()
    # host = request.user
    total =  get_total(products)
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(total),
        'item_name': str([product.name+'\n' for product in products]),
      #  'invoice': str([product.name+'\n' for product in Product.objects.all()])
        'currency_code': 'USD',
    }
   
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'store/payment.html', {'order': products,
     'form': form,
     'page':'process',
     'total':total})


@csrf_exempt
def payment_done(request):
    return render(request, 'store/payment.html',{'page':'done'})

@csrf_exempt
def payment_cancelled(request):
    return render(request, 'store/payment.html',{'page':'cancelled'})