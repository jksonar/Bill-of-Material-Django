from django.contrib import admin
from .models import Order, BOMFabric, BOMAccessory, BOMVersion

class BOMFabricInline(admin.TabularInline):
    model = BOMFabric
    extra = 0
    readonly_fields = ('required_qty', 'balance')
    raw_id_fields = ('fabric', 'version')

class BOMAccessoryInline(admin.TabularInline):
    model = BOMAccessory
    extra = 0
    readonly_fields = ('required_qty', 'balance')
    raw_id_fields = ('accessory', 'version')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'customer', 'style', 'quantity', 'due_date', 'status')
    list_filter = ('status', 'due_date', 'style')
    search_fields = ('order_no', 'customer', 'style__name')
    inlines = [BOMFabricInline, BOMAccessoryInline]

@admin.register(BOMFabric)
class BOMFabricAdmin(admin.ModelAdmin):
    list_display = ('order', 'version', 'fabric', 'required_qty', 'issued_qty', 'balance')
    list_filter = ('order__style', 'fabric', 'version')
    search_fields = ('order__order_no', 'fabric__name')
    readonly_fields = ('required_qty', 'balance')

@admin.register(BOMAccessory)
class BOMAccessoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'version', 'accessory', 'required_qty', 'issued_qty', 'balance')
    list_filter = ('order__style', 'accessory', 'version')
    search_fields = ('order__order_no', 'accessory__name')
    readonly_fields = ('required_qty', 'balance')

@admin.register(BOMVersion)
class BOMVersionAdmin(admin.ModelAdmin):
    list_display = ('order', 'version_number', 'created_at', 'notes')
    list_filter = ('order', 'created_at')
    search_fields = ('order__order_no', 'notes')
