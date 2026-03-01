from django.contrib import admin
from .models import Category, Product, Wishlist


# ----------------------------
# CATEGORY ADMIN
# ----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


# ----------------------------
# PRODUCT ADMIN
# ----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'stock',
        'is_active',
        'created_at'
    )

    list_filter = (
        'is_active',
        'created_at',
        'category'
    )

    search_fields = (
        'name',
        'description',
        'category__name'
    )

    prepopulated_fields = {'slug': ('name',)}

    ordering = ('-created_at',)

    list_editable = (
        'price',
        'stock',
        'is_active'
    )

    readonly_fields = ('created_at', 'updated_at')


# ----------------------------
# WISHLIST ADMIN
# ----------------------------
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'created_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)