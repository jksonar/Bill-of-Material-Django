from django.contrib import admin
from .models import Fabric, Accessory, Color, FabricColor, AccessoryColor

class FabricColorInline(admin.TabularInline):
    model = FabricColor
    extra = 1

class FabricAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description', 'construction', 'composition', 'supplier', 'stock_in_hand', 'width', 'weight', 'lead_time', 'unit_price')
    search_fields = ('name', 'code', 'description', 'supplier', 'construction', 'composition')
    list_filter = ('supplier', 'construction', 'composition')
    inlines = [FabricColorInline]

class AccessoryColorInline(admin.TabularInline):
    model = AccessoryColor
    extra = 1

class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description', 'finish', 'supplier', 'price', 'weight', 'unit', 'lead_time', 'stock')
    search_fields = ('name', 'code', 'supplier', 'description', 'finish')
    list_filter = ('supplier', 'finish', 'unit')
    inlines = [AccessoryColorInline]

admin.site.register(Fabric, FabricAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Color)
