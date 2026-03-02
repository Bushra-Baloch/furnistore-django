from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Order


# ----------------------------
# ORDER LIST (User Orders)
# ----------------------------
@login_required
def order_list(request):
    order_list = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related('items')
        .order_by('-created_at')
    )

    paginator = Paginator(order_list, 5)  # 5 orders per page
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    return render(request, 'orders/order_list.html', {
        'orders': orders
    })


# ----------------------------
# ORDER DETAIL
# ----------------------------
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        id=order_id,
        user=request.user
    )

    return render(request, 'orders/order_detail.html', {
        'order': order
    })


# ----------------------------
# ORDER SUCCESS
# ----------------------------
@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')