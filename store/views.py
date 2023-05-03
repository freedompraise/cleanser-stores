#DJANGO
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponseRedirect , reverse
from django.contrib.auth.forms import AuthenticationForm
#APP
from .models import Product
#PAYPAL
from paypal.standard.forms import PayPalPaymentsForm

from random import sample


# Create your views here.
def get_total(request,products):
    total_int = int()
    # calculating for total in all products by multiplying their price with quantity
    for product in products:
        product.discount = float(str(0.13 * float(product.price))[:4])
        # assigning a quantity for each item in the cart page
        product.order=request.POST.get(product.name) if request.POST.get(product.name) else product.order
        # determining total - the product of price and the quantity of product
        product.total = float(str(float(product.order) * float(product.price))[:4])
        total_int += product.total
        product.save()
      
    return total_int

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
    count = user.product_set.all().count()
    all_products = list(Product.objects.all())
    random_objects = sample(all_products, 2)
    total_int= round(get_total(request,products),2)


    context={"products":products, "total":total_int,'count':count, 'random_products':random_objects}
    return render(request,'store/checkout.html',context)


@login_required(login_url='login')
def cart(request):
    user=request.user
    products = user.product_set.all()
    total_int = round(get_total(request, products),3)

    context={"products":products, "total":total_int}
    return render(request,'store/cart.html',context) 


def product_delete(request, pk):
  # get the product object
    product = Product.objects.get(id=pk)
    user = request.user
  # delete the product
    product.customers.remove(user)
    product.save()
  # redirect to the product list page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('cart')))

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authenticate the user with the provided email and password
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Welcome back! You are now logged in.')
                return HttpResponseRedirect(request.META.get('store', reverse('store')))
            else:
                messages.error(request,'Invalid Login credentials')
                return redirect('login')
        return redirect('login')
            
    return render(request,'store/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']        
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('register')
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            auth_login(request, user)
            return HttpResponseRedirect(request.META.get('store', reverse('store')))
    return render(request, 'store/register.html')

    # PAYPAL

def process_payment(request):
    user = request.user
    products = user.product_set.all()
    total_int = get_total(request, products)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(total_int),
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