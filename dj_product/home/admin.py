from django.contrib import admin
from django.db import models
from .models import ProductCategory, Product, CartItems, Cart
from django.utils.html import format_html

# Register your models here.

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name",)
    fields = ("category_name",)
    save_on_top = True
    list_per_page =2

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("show_Product_Image",)
    list_display = ("category","product_name","price","show_Product_Image","categoryname")
    fields       = ("category","product_name","image","price","show_Product_Image")
    save_on_top = True
    list_per_page =2

    def categoryname(self, obj):
        return "Hello"

    def show_Product_Image(self,obj):
        #print(obj)
        #return format_html(f'<img width="50px" height="50px" src="{obj.featured_image.url}"/>')
        return format_html('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=60,
            height=50,
            )
        )

class CartItemsAdmin(admin.ModelAdmin):
    list_display = ("product","cart")
    fields = ("product","cart")
    save_on_top = True
    list_per_page =10

class CartAdmin(admin.ModelAdmin):
    list_display = ("user",)
    fields = ("user",)
    save_on_top = True
    list_per_page =10

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItems, CartItemsAdmin)
admin.site.register(Cart, CartAdmin)