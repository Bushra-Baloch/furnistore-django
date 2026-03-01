from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, Category, Wishlist
from orders.models import Order, OrderItem
from cart.cart import Cart
@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            city=request.POST['city'],
            total_price=cart.get_total_price()
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()
        return redirect('order_success')

    return render(request, 'shop/checkout.html', {'cart': cart})


@login_required
def order_success(request):
    return render(request, 'shop/order_success.html')


def home(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.all()

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'categories': categories
    })


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    categories = Category.objects.all()

    return render(request, 'shop/category.html', {
        'category': category,
        'products': products,
        'categories': categories
    })


def winter_sale(request):
    categories = Category.objects.all()
    return render(request, 'shop/winter_sale.html', {
        'categories': categories
    })





@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            city=request.POST['city'],
            total_price=cart.get_total_price()
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()
        return redirect('order_success')

    return render(request, 'shop/checkout.html', {'cart': cart})





@login_required
def add_to_wishlist(request, product_id):
    Wishlist.objects.get_or_create(
        user=request.user,
        product_id=product_id
    )
    return redirect('wishlist')


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'shop/wishlist.html', {'items': items})


@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()
    return redirect('wishlist')
