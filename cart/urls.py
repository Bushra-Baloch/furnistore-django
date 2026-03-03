from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    # Cart Pages
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('decrease/<int:product_id>/', views.cart_decrease, name='cart_decrease'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),

    # Payment
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('success/', views.payment_success, name='success'),
]