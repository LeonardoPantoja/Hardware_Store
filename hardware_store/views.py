from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, ProductCategory, Cart, CartItem
from .forms import ProductForm, CategoryForm, PaymentForm
from django.urls import reverse

from django.http import JsonResponse

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect
from collections.abc import Iterable
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import stripe


# Product
PRODUCT_LIST_PATH = '/product_list'

def product_list(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    if not isinstance(categories, Iterable):

        categories = []
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'product_list.html', context)


def create_product(request):
    if 'user_id' not in request.session:
        return redirect(PRODUCT_LIST_PATH)
    if not request.user.is_authenticated:
        return redirect(PRODUCT_LIST_PATH)
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect(PRODUCT_LIST_PATH)
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})


def edit_product(request, pk):
    if 'user_id' not in request.session:
        return redirect(PRODUCT_LIST_PATH)
    if not request.user.is_authenticated:
        return redirect(PRODUCT_LIST_PATH)
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect(PRODUCT_LIST_PATH)
    return render(request, 'edit_product.html', {'form': form, 'product': product})


def delete_product(request, pk):
    if 'user_id' not in request.session:
        return redirect(PRODUCT_LIST_PATH)
    if not request.user.is_authenticated:
        return redirect(PRODUCT_LIST_PATH)
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect(PRODUCT_LIST_PATH)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


# Category
CATEGORY_LIST_PATH = '/category_list'


def category_list(request):
    category = ProductCategory.objects.all()
    return render(request, 'category_list.html', {'category': category})


def create_category(request):
    if 'user_id' not in request.session:
        return redirect(CATEGORY_LIST_PATH)
    if not request.user.is_authenticated:
        return redirect(CATEGORY_LIST_PATH)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect(CATEGORY_LIST_PATH)
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})


def edit_category(request, pk):
    if 'user_id' not in request.session:
        return redirect(CATEGORY_LIST_PATH)
    if not request.user.is_authenticated:
        return redirect(CATEGORY_LIST_PATH)
    category = get_object_or_404(ProductCategory, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        category = form.save(commit=False)
        category.save()
        return redirect(CATEGORY_LIST_PATH)

    return render(request, 'edit_category.html', {'form': form})


def delete_category(request, pk):
    if 'user_id' not in request.session:
        return redirect(CATEGORY_LIST_PATH)
    if not request.user.is_authenticated:
        return redirect(CATEGORY_LIST_PATH)
    category = get_object_or_404(ProductCategory, pk=pk)
    category.delete()
    return redirect(CATEGORY_LIST_PATH)


def category_products(request, pk):
    category = ProductCategory.objects.get(pk=pk)
    products = Product.objects.filter(category_id=category)
    categories = ProductCategory.objects.all()
    
    paginator = Paginator(products, 12) 
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'category': category,
        'products': products
    }
    
    if products.has_previous():
        context['prev_page'] = products.previous_page_number()
    if products.has_next():
        context['next_page'] = products.next_page_number()
    
    context['total_pages'] = paginator.num_pages
    return render(request, 'product_list.html', context)

# Home


def home(request):
    return render(request, 'home.html')

stripe.api_key = 'sk_test_51OG73FIrydiWNqtYFVV9f5CQV7HUJAOkybJMM67OP0VMixNFPTmJnhUp72yf0uQCmJXJXsDKSvteAuCXT9dQjKJj00UINb3SA4'

def calcular_total_carrito(user):
    user_cart = Cart.objects.get_or_create(user=user)[0]
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(item.subtotal() for item in cart_items)
    return total_price

@login_required
def checkout(request):
    total_carrito = None

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                token = form.cleaned_data['stripe_token']

                # Obtener o crear el carrito del usuario
                user_cart, cart_created = Cart.objects.get_or_create(user=request.user)

                # Calcular el total del carrito
                cart_items = user_cart.cartitem_set.all()
                total_carrito = sum(item.product.price * item.quantity for item in cart_items)

                amount_in_cents = int(total_carrito * 100)

                # Crear una sesión de pago con Stripe Checkout
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'mxn',
                            'product_data': {
                                'name': 'Compra en tu tienda',
                            },
                            'unit_amount': amount_in_cents,
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('cart')),
                    cancel_url=request.build_absolute_uri('cancel_url'),
                )

                return JsonResponse({'session_id': checkout_session.id})
            except stripe.error.CardError as e:
                return JsonResponse({'error': str(e)})
            except Exception as e:
                return JsonResponse({'error': str(e)})
    else:
        form = PaymentForm()

    return render(request, 'checkout.html', {'form': form, 'total_carrito': total_carrito})

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('category-list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] =  user.id
                return redirect(CATEGORY_LIST_PATH)
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid user'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    logout(request)
    return redirect('category_list')


def product_list(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    if not isinstance(categories, Iterable):
        categories = []
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'products': products
    }
    
    if products.has_previous():
        context['prev_page'] = products.previous_page_number()
    if products.has_next():
        context['next_page'] = products.next_page_number()
    
    context['total_pages'] = paginator.num_pages
    
    return render(request, 'product_list.html', context)


@login_required
def cart(request):
    user_cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(item.subtotal() for item in cart_items)

    return render(request, 'cart.html', {'cart': user_cart, 'total_price': total_price})

@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.subtotal() for item in cart_items)

    return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if product.stock >= 1:
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
        
        product.stock -= 1
        product.save()

        return redirect('cart')
    else:
        messages.error(request, 'No hay suficiente stock disponible para este producto.')
        return redirect('product_list') 

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    user_cart = Cart.objects.get(user=request.user)

    try:
        cart_item = CartItem.objects.get(cart=user_cart, product=product)
        quantity_before_removal = cart_item.quantity
        cart_item.delete()

        product.stock += quantity_before_removal
        product.save()

        messages.success(request, 'Producto eliminado del carrito.')
    except CartItem.DoesNotExist:
        messages.error(request, 'El producto no está en tu carrito.')

    return redirect('cart')

