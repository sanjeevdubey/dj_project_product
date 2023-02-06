from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
#from locust import User
from django.contrib.auth import login,authenticate,logout
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import secrets
import math

# Create your views here.
@login_required(login_url='/login')
def home(request):
    productlist = Product.objects.all()
    context = {"productlist": productlist}
    return render(request, 'home/home.html', context)


def register_page(request):
    if request.method == 'POST': 
        #print(request.POST) 
        username     =  request.POST.get('username')
        email        =  request.POST.get('email')
        password     =  request.POST.get('password')
        fname        =  request.POST.get('first_name')
        lname        =  request.POST.get('last_name')      
        try:                     
            obj_user     =  list(User.objects.filter(username = username))
            #print(obj_user)
            if username not in obj_user:
                messages.success(request, 'User Registered Succesfully. Now You can login')
                #obj_user =  User.objects.create(username = username, email=email,first_name=fname, last_name=lname)
                obj_user =  User(username = username, email = email, first_name=fname, last_name=lname)
                #obj_user.set_password(password = password)
                obj_user.set_password(password)
                obj_user.save()
                return redirect('/login')               
            else:
                messages.error(request, 'Usernname Already Exits.')
                return redirect('/register')                
        except:
            messages.error(request, 'Something Went Wrong.')
            return redirect('/register')
    else:
        return render(request, 'home/register.html')

def login_page(request):
    if request.POST:          
        try:          
            username     =  request.POST.get('username')
            password =  request.POST.get('password')
            #obj_user =  User.objects.filter(username)
            user = authenticate(request, username=username, password=password)
            pass
            if user is not None:
                form = login(request, user)
                messages.error(request, 'Welcome to the web page')
                return redirect('cartpage')
               
                #return redirect('home/carts.html')
            else:
                messages.error(request, 'Seems Wrong user name or password')
                return redirect('/login') 
                
                #return redirect('/')
        except:
            return redirect('/')
    return render(request, 'home/login.html')
    
@login_required(login_url='/login')
def add_cart(request, product_id):
    user = request.user
    product_obj = Product.objects.get(uid=product_id)
    cart, _= Cart.objects.get_or_create(user=user, is_paid=False)
    cart_items = CartItems.objects.create(
        cart = cart,
        product = product_obj
    )

    return redirect('/')        
@login_required(login_url='/login')
def cartpage(request,):
    cart = Cart.objects.get(is_paid=False, user= request.user)
    payment_ref_id_genrated =   secrets.token_urlsafe(math.floor(32 / 1.3))  # Creating dummy PaymentID
    cart.payment_ref_id = payment_ref_id_genrated
    cart.save()
    context =  {'carts': cart, 'code':payment_ref_id_genrated, 'paymentlink' : '/paidcheck/ordersuccess'}
    return render(request, 'home/carts.html', context)
    #return redirect('/')    

def logoutlink(request,):
    logout(request)
    messages.error(request, 'Logged Out Successfully')
    return redirect('/login')
    #return redirect('/')        

@login_required(login_url='/login')
def remove_cart_item(request, cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()
        return redirect('/cart-page')
    except Exception as e:
        print(e)

@login_required(login_url='/login')
def order(request,):
    ordered_item=  Cart.objects.filter(is_paid=True, user=request.user)
    context = {'orders': ordered_item}
    return render(request, 'home/order.html', context)


@login_required()
def ordersuccess(request):
    
    payment_ref_id = request.GET.get('paidid')
    cart =  Cart.objects.get(payment_ref_id=payment_ref_id)
    cart.is_paid=True
    cart.save()
    return redirect('/order-page')

