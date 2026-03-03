from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from shop.models import Product
from orders.models import Order, OrderItem

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# --------------------------------
# HELPER FUNCTION
# --------------------------------
def calculate_cart_total(cart):
    return sum(
        Decimal(item['price']) * item['quantity']
        for item in cart.values()
    )


# --------------------------------
# CART DETAIL
# --------------------------------
@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    total = calculate_cart_total(cart)

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'total': total
    })


# --------------------------------
# ADD TO CART
# --------------------------------
@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, "Product is out of stock.")
        return redirect('cart_detail')

    cart = request.session.get('cart', {})
    pid = str(product.id)

    if pid in cart:
        if cart[pid]['quantity'] < product.stock:
            cart[pid]['quantity'] += 1
        else:
            messages.warning(request, "Stock limit reached.")
    else:
        cart[pid] = {
            'product_id': product.id,
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
        }

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


# --------------------------------
# DECREASE QUANTITY
# --------------------------------
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


# --------------------------------
# REMOVE ITEM
# --------------------------------
@login_required
def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


# --------------------------------
# CHECKOUT
# --------------------------------
@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart_detail')

    total = calculate_cart_total(cart)

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
                product_id=int(pid),
                price=Decimal(item['price']),
                quantity=item['quantity']
            )

            # Reduce stock
            product = Product.objects.get(id=pid)
            product.stock -= item['quantity']
            product.save()

        # Send email
        send_mail(
            subject='Order Confirmation - FurniStore',
            message=f"""
Thank you for your order!

Order ID: {order.id}
Total Amount: ${order.total_price}

We appreciate your business.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=True
        )

        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('orders:order_success')

    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'total': total
    })


# --------------------------------
# STRIPE PAYMENT
# --------------------------------
@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    intent = stripe.PaymentIntent.create(
        amount=int(order.total_price * 100),
        currency='usd',
        metadata={'order_id': order.id}
    )

    return render(request, 'cart/payment.html', {
        'client_secret': intent.client_secret,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'order': order
    })


# --------------------------------
# PAYMENT SUCCESS
# --------------------------------
def payment_success(request):
    return render(request, 'cart/success.html')