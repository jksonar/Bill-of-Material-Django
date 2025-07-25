from django.contrib import admin
from .models import Order, BOMFabric, BOMAccessory, BOMVersion, OrderItem
from guardian.admin import GuardedModelAdmin

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ('style_variant',)

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
class OrderAdmin(GuardedModelAdmin):
    list_display = ('order_no', 'customer', 'customer_po_no', 'style', 'delivery_date', 'destination', 'season', 'shipment_mode', 'status')
    list_filter = ('status', 'delivery_date', 'style', 'season', 'shipment_mode')
    search_fields = ('order_no', 'customer', 'customer_po_no', 'style__name')
    inlines = [OrderItemInline, BOMFabricInline, BOMAccessoryInline]

@admin.register(BOMFabric)
class BOMFabricAdmin(GuardedModelAdmin):
    list_display = ('order', 'version', 'fabric', 'required_qty', 'issued_qty', 'balance')
    list_filter = ('order__style', 'fabric', 'version')
    search_fields = ('order__order_no', 'fabric__name')
    readonly_fields = ('required_qty', 'balance')

@admin.register(BOMAccessory)
class BOMAccessoryAdmin(GuardedModelAdmin):
    list_display = ('order', 'version', 'accessory', 'required_qty', 'issued_qty', 'balance')
    list_filter = ('order__style', 'accessory', 'version')
    search_fields = ('order__order_no', 'accessory__name')
    readonly_fields = ('required_qty', 'balance')

@admin.register(BOMVersion)
class BOMVersionAdmin(GuardedModelAdmin):
    list_display = ('order', 'version_number', 'created_at', 'notes')
    list_filter = ('order', 'created_at')
    search_fields = ('order__order_no', 'notes')
