from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()


# ----------------------------
# CATEGORY MODEL
# ----------------------------
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, db_index=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_by_category', args=[self.slug])


# ----------------------------
# PRODUCT MODEL
# ----------------------------
class Product(models.Model):
    id = models.BigAutoField(primary_key=True)

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=260, unique=True, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def is_in_stock(self):
        return self.stock > 0


# ----------------------------
# WISHLIST MODEL
# ----------------------------
class Wishlist(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"