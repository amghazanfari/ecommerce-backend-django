from django.contrib import admin
from store.models import Product, Category, Gallery, Specification,\
                              Size, Color, Cart, CartOrder, CartOrderItem,\
                              ProductFaq, Review, WhishList, Notification, Coupon

class GalleryInline(admin.TabularInline):
    model = Gallery

class SpecificationInline(admin.TabularInline):
    model = Specification

class SizeInline(admin.TabularInline):
    model = Size

class ColorInline(admin.TabularInline):
    model = Color

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "product_category", "shipping_amount", "stock", "in_stock", "product_vendor", "featured"]
    list_editable = ["featured"]
    list_filter = ["date"]
    search_fields = ["title"]
    inlines = [GalleryInline, SpecificationInline, SizeInline, ColorInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartOrder)
admin.site.register(CartOrderItem)
admin.site.register(ProductFaq)
admin.site.register(Review)
admin.site.register(WhishList)
admin.site.register(Notification)
admin.site.register(Coupon)
