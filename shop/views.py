from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Product, Category, Wishlist


# ----------------------------
# HOME PAGE (WITH PAGINATION)
# ----------------------------
def home(request):
    product_list = (
        Product.objects
        .select_related('category')
        .filter(is_active=True)
        .only('id', 'name', 'slug', 'price', 'image', 'category')
        .order_by('-created_at')
    )

    paginator = Paginator(product_list, 6)  # 6 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = Category.objects.only('id', 'name', 'slug')

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories
    })


# ----------------------------
# PRODUCT DETAIL
# ----------------------------
def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        slug=slug,
        is_active=True
    )

    categories = Category.objects.only('id', 'name', 'slug')

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'categories': categories
    })


# ----------------------------
# CATEGORY PRODUCTS
# ----------------------------
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)

    product_list = (
        Product.objects
        .select_related('category')
        .filter(category=category, is_active=True)
        .only('id', 'name', 'slug', 'price', 'image')
        .order_by('-created_at')
    )

    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = Category.objects.only('id', 'name', 'slug')

    return render(request, 'shop/category.html', {
        'category': category,
        'products': products,
        'categories': categories
    })


# ----------------------------
# WINTER SALE PAGE
# ----------------------------
def winter_sale(request):
    categories = Category.objects.only('id', 'name', 'slug')
    return render(request, 'shop/winter_sale.html', {
        'categories': categories
    })


# ----------------------------
# WISHLIST
# ----------------------------
@login_required
def add_to_wishlist(request, product_id):
    Wishlist.objects.get_or_create(
        user=request.user,
        product_id=product_id
    )
    return redirect('wishlist')


@login_required
def wishlist(request):
    items = (
        Wishlist.objects
        .filter(user=request.user)
        .select_related('product')
    )

    return render(request, 'shop/wishlist.html', {
        'items': items
    })


@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()

    return redirect('wishlist')