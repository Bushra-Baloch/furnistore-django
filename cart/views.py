from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from shop.models import Product
from orders.models import Order, OrderItem

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# ----------------------------
# PAYMENT SUCCESS
# ----------------------------
def payment_success(request):
    return render(request, 'cart/success.html')


# ----------------------------
# STRIPE PAYMENT
# ----------------------------
@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    intent = stripe.PaymentIntent.create(
        amount=int(order.total_price * 100),  # convert to cents
        currency='usd',
        metadata={'order_id': order.id}
    )

    return render(request, 'cart/payment.html', {
        'client_secret': intent.client_secret,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'order': order
    })


# ----------------------------
# CART DETAIL
# ----------------------------
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart_detail')

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            total_price=total
        )

        for pid, item in cart.items():
            OrderItem.objects.create(
                order=order,
                product_id=pid,
                price=item['price'],
                quantity=item['quantity']
            )

        # Send confirmation email
        send_mail(
            subject='Order Confirmation - FurniStore',
            message=f"""
Thank you for your order!

Order ID: {order.id}
Total Amount: ${order.total_price}

We will contact you soon.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=False
        )

        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('orders:order_success')

    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'total': total
    })