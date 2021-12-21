from django.contrib import admin

# Register your models here.

from .models import Product, ProductImg

# admin.site.register(Product)
# admin.site.register(ProductImg)

class ProductImgInline(admin.StackedInline):
    model = ProductImg
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImgInline,]

admin.site.register(Product,ProductAdmin)
