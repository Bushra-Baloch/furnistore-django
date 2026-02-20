from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Product
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .cart import Cart
from shop.models import Order, OrderItem
from django.core.mail import send_mail
def payment_success(request):
    return render(request, 'cart/success.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Product, Order, OrderItem
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment(request, order_id):
    order = Order.objects.get(id=order_id)

    intent = stripe.PaymentIntent.create(
        amount=int(order.get_total_price() * 100),  # cents
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
@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart_detail')

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            city=request.POST['city'],
            total_price=total
        )

        for pid, item in cart.items():
            OrderItem.objects.create(
                order=order,
                product_id=pid,
                price=item['price'],
                quantity=item['quantity']
            )

        # ✅ SEND EMAIL (console ke liye)
        send_mail(
            subject='Order Confirmation - FurniStore',
            message=f'''
Thank you for your order!

Order ID: {order.id}
Total Amount: ${order.total_price}

We will contact you soon.
''',
            from_email='noreply@furnistore.com',
            recipient_list=[order.email],
            fail_silently=True

        )

        # ✅ CART CLEAR HERE ONLY
        request.session['cart'] = {}

        return redirect('order_success')

    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'total': total
    })
