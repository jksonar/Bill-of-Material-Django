from django.contrib import admin
from .models import Fabric, Accessory, Inventory, Color, FabricColor, AccessoryColor

class FabricColorInline(admin.TabularInline):
    model = FabricColor
    extra = 1

class FabricAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'type', 'supplier', 'unit_price', 'gsm', 'width')
    search_fields = ('name', 'code', 'supplier', 'type')
    list_filter = ('type', 'supplier')
    inlines = [FabricColorInline]

class AccessoryColorInline(admin.TabularInline):
    model = AccessoryColor
    extra = 1

class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'type', 'supplier', 'unit_price')
    search_fields = ('name', 'code', 'supplier', 'type')
    list_filter = ('type', 'supplier')
    inlines = [AccessoryColorInline]

admin.site.register(Fabric, FabricAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Inventory)
admin.site.register(Color)
