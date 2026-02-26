from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


def list(request):
    
    cat_id=request.GET.get('category_id')
    search_query = request.GET.get('search')

    products = Product.objects.all()
    if cat_id:
        filterd_products = Product.objects.filter(category_id=cat_id)

    
    if search_query:
        products = products.filter(name_icontains=search_query)
    context={
        'prod':filterd_products
    }
    return render(request,'products/list.html',context)



def add_to_cart(request, pid):
    prod = get_object_or_404(Product, pk=pid)
    cart = request.session.get('cart', {})
    pid_str = str(pid) 

    if pid_str in cart:
        cart[pid_str]['quantity'] += 1
    else:
        cart[pid_str] = {
            'id': pid,
            'name': prod.name,
            'price': float(prod.price),
            'quantity': 1,
            'image': prod.image.url if hasattr(prod, 'image') else ''  
        }

    request.session['cart'] = cart
    request.session['cart_count'] = sum(item['quantity'] for item in cart.values())
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def cart_view(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['quantity'] * item['price'] for item in cart.values())
    
    context = {
        "cart": cart,
        "total_price": total_price
    }
    return render(request, "products/cart.html", context)

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_view')
        
    total_price = sum(item['quantity'] * item['price'] for item in cart.values())
    
    context = {
        "cart": cart,
        "total_price": total_price,
        "company_name": "متجر الجوهرة",
    }
    return render(request, "products/checkout.html", context)

@login_required
def create_invoice(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        customer_name = request.POST.get('customer_name')
        total_price = request.POST.get('total_price')
        
        context = {
            "customer_name": customer_name,
            "cart": cart,
            "total_price": total_price,
            "company_name": "متجر الجوهرة",
            "date": "2026-02-26",
        }
        request.session['cart'] = {}
        request.session['cart_count'] = 0
        
        return render(request, "products/invoice.html", context)
    return redirect('checkout')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success') 
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('category_index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('category_index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('category_index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})