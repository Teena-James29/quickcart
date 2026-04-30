from django.shortcuts import render,redirect
from .models import category, Product, Profile,Order,OrderItem
from .forms import ProductForm, Profileform
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required 


# Create your views here.


@login_required(login_url='/login') 
def homefn(request):
    categories = category.objects.all() 
    products = Product.objects.all()

    context = {
        'category': categories,  
        'a': products
    }
    return render(request, 'home.html', context) 



@login_required(login_url='/login')
def profilefn(request):   
    if Profile.objects.filter(us=request.user).exists():
        prof = Profile.objects.get(us=request.user)
        products = Product.objects.filter(us=request.user)

        return render(request, 'profile.html', {
            'profile': prof,
            'products': products
        })
    else:
        return redirect('/addprofile')


    

from django.contrib.auth import authenticate, login
from django.contrib import messages

def loginfn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

    


def formfn(request):
     return render(request,'form.html')



def logoutfn(request):
    auth.logout(request)
    return redirect('/login')

def registerfn(request):
    if request.method=='POST':
        u=request.POST['uname']
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['em']
        p1=request.POST['p']
        p2=request.POST['ps']

        if p1 == p2:
            if User.objects.filter(username=u).exists():
                return render(request, 'register.html', {'er': "username already exists"})
            elif User.objects.filter(email=e).exists():
                return render(request, 'register.html', {'er': "email already exists"})
            else:
                User.objects.create_user(username=u, email=e, first_name=f, last_name=l, password=p1)
                return redirect('/login')
        else:
            return render(request, 'register.html', {'er': "password not matching"})
    else:
        return render(request, 'register.html')
    

def aboutfn(request):
    return render(request,'about.html')


def addproductfn(request):
    if request.method=='POST':
         f=ProductForm(request.POST,request.FILES)
         if f.is_valid():
             x=f.save(commit=False)
             x.us=request.user
             x.save()
             return redirect('/')
    else:
        f=ProductForm()
        return render(request,'addproduct.html',{'fm':f})




def viewcategoryfn(request,cid):
    x = Product.objects.filter(ctry=cid)
    return render(request, 'viewcategory.html', {'pro': x})

def viewproductfn(request,pid):
    x=Product.objects.get(id=pid)
    return render(request,'viewproduct.html',{'pro':x})


def addprofilefn(request):
    if request.method=='POST':
        f=Profileform(request.POST,request.FILES)
        if f.is_valid():
            x=f.save(commit=False)
            x.us=request.user
            x.save()
            return redirect('/profile')
    else:
        f=Profileform()
        return render(request,'addprofile.html',{'fm':f})
    

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def editproductfn(request, pid):

    product = get_object_or_404(Product, id=pid, us=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm(instance=product)

    return render(request, 'editproduct.html', {'fm': form})

@login_required
def deletefn(request, pid):
    product = get_object_or_404(Product, id=pid, us=request.user)

    product.delete()
    return redirect('/profile')




from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()

    context = {
        'cart': cart,
        'items': items,
    }

    return render(request, 'cart.html', context)

from django.shortcuts import get_object_or_404, redirect, render

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('view_cart')


@login_required
def update_quantity(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == "increase":
        item.quantity += 1
        item.save()

    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    return redirect('view_cart')

def userprofilefn(request,uid):
    u=User.objects.get(id=uid)
    x=Product.objects.filter(us=uid)
    return render(request,'userprofile.html',{'us':u,'pro':x}) 


from django.contrib.auth.decorators import login_required

@login_required
def editprofilefn(request):

    profile = request.user.profile   
    if request.method == 'POST':
        f = Profileform(request.POST, request.FILES, instance=profile)
        if f.is_valid():
            f.save()
            return redirect('/profile/')
    else:
        f = Profileform(instance=profile)

    return render(request, 'editprofile.html', {'fm': f})



@login_required
def buynowfn(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.cartitem_set.all()

    if not items:
        return redirect('view_cart')

    total = 0
    for item in items:
        total += item.total_price()


    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

   
    items.delete()

    return render(request, 'success.html', {'order': order})