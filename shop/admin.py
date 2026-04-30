from django.contrib import admin

# Register your models here.

from .models import Product,category,Profile

admin.site.register(Product)
admin.site.register(category)
admin.site.register(Profile)