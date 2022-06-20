from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages
from .forms import ProductForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def store(request):
    all = Product.objects.all()
    context={'all':all}
    return render(request,'store/store.html',context)

def product_page(request,pk):
    product=Product.objects.get(id=pk)
    discount=str(0.83*float(product.price))
    save=str(0.17*float(product.price))
    context={"product":product,'discount':discount[:4],'save':save[:4]}

    return render(request,'store/product.html',context)

def checkout(request):
    context = {}
    return render(request,'store/checkout.html',context)

def cart(request):
    user=request.user
    products = user.product_set.all()
    total_dict={}
    if request.method=="POST":
        id=request.POST.get('id')
        product=Product.objects.get(id=id)
        quantity=request.POST.get('quantity')
        if quantity:
            product.order=quantity
            product.save()


    for product in products:
        if product.order:
            product.total=product.order * product.price
            product.save()
            total_dict[product.id]=product.total
    total_int=int()
    discount=int()
    for value in total_dict.values():
        total_int+=value
        
    discount=str(0.13*float(total_int))
    discount=discount.split('.')


    context={"products":products, "total":total_int,'discount':discount[0]+'.'+discount[1][:2]}
    return render(request,'store/cart.html',context) 

def delete(request,pk):
    product=Product.objects.get(id=pk)
    context={"product":product}
    if request.method=="POST":
        product.delete()
        return redirect('cart')
    return render(request,'store/delete.html', context) 


def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,'User not registered')
            
        user=authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('store')
        else:  
            messages.error(request,'Username or Password not correct')
            
    return render(request,'store/login.html')


def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password') 
        User.objects.create(
            username=username,
            email=email,
            password=password
        )
        return redirect('store')
    context={'page':'register'}
    return render(request,'store/register.html')