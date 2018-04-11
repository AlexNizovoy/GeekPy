from django.contrib import admin

from product.models import Currency, Category, Subcategory, Product, Vendor, ProductPropertiesKeys, ProductPropertiesValues

# Register your models here.
admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(ProductPropertiesKeys)
admin.site.register(ProductPropertiesValues)
