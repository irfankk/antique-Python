from django.contrib import admin

from apps.catalogue.models import Product

class ProductAdmin(admin.ModelAdmin):
	models = Product


admin.site.register(Product, ProductAdmin)
