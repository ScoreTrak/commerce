from django.contrib import admin

from ldfinance.shop.models import Order, Product, Question


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


class QuestionInline(admin.StackedInline):
    model = Question


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("name", "price", "is_published")
