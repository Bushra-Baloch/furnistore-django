from django.contrib import admin

# Register your models here.

from .models import Category, Product


from .models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active', 'category')
    prepopulated_fields = {'slug': ('name',)}

    
from .models import Wishlist

admin.site.register(Wishlist)
