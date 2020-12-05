from django.contrib import admin

from ldfinance.shop.models import Order, Product


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_published")
