from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Product
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .cart import Cart
from shop.models import Order, OrderItem
from django.core.mail import send_mail



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Product, Order, OrderItem


# ----------------------------
# CART DETAIL
# ----------------------------
@login_required(login_url='login')
def cart_detail(request):
    cart = request.session.get('cart', {})
    total = sum(
        item['price'] * item['quantity']
        for item in cart.values()
    )

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'total': total
    })


# ----------------------------
# ADD TO CART
# ----------------------------
@login_required(login_url='login')
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    pid = str(product.id)

    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
        }

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


# ----------------------------
# DECREASE QUANTITY
# ----------------------------
@login_required(login_url='login')
def cart_decrease(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        cart[pid]['quantity'] -= 1
        if cart[pid]['quantity'] <= 0:
            del cart[pid]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


# ----------------------------
# REMOVE ITEM
# ----------------------------
@login_required(login_url='login')
def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


# ----------------------------
# CHECKOUT
# ----------------------------
@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart_detail')

    total = sum(
        item['price'] * item['quantity']
        for item in cart.values()
    )

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            total_price=total
        )

        for item in cart.values():
            product = Product.objects.get(id=item['product_id'])

            OrderItem.objects.create(
                order=order,
                product=product,
                price=item['price'],
                quantity=item['quantity']
            )

        # ✅ CLEAR CART AFTER ORDER
        request.session['cart'] = {}
        request.session.modified = True

        # 🔜 EMAIL CAN BE ADDED HERE LATER

        return redirect('order_success')

    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'total': total
    })
