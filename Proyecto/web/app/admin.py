from django.contrib import admin
from .models import Client, Module, Product, Purchase, selectedModules

# Register your models here.
admin.site.register(Client)
admin.site.register(Module)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(selectedModules)