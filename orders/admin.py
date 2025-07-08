from django.contrib import admin
from .models import Order, BOMFabric, BOMAccessory

admin.site.register(Order)
admin.site.register(BOMFabric)
admin.site.register(BOMAccessory)
