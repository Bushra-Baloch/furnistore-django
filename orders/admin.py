from django.contrib import admin
from .models import Order, OrderItem


# ----------------------------
# ORDER ITEM INLINE
# ----------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')


# ----------------------------
# ORDER ADMIN
# ----------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'full_name',
        'email',
        'status',
        'total_price',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'user__username',
        'email',
        'full_name',
    )

    ordering = ('-created_at',)

    inlines = [OrderItemInline]


# ----------------------------
# ORDER ITEM ADMIN
# ----------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'order',
        'product',
        'price',
        'quantity',
    )

    search_fields = (
        'product__name',
        'order__id',
    )