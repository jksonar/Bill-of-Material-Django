from django.contrib import admin
from .models import FabricPO, FabricPOItem, FabricReceipt, FabricReceiptItem
from guardian.admin import GuardedModelAdmin

class FabricPOItemInline(admin.TabularInline):
    model = FabricPOItem
    extra = 1
    raw_id_fields = ('fabric',)

@admin.register(FabricPO)
class FabricPOAdmin(GuardedModelAdmin):
    list_display = ('po_no', 'supplier', 'date', 'delivery_date', 'total_qty', 'status')
    list_filter = ('status', 'supplier', 'date', 'delivery_date')
    search_fields = ('po_no', 'supplier')
    inlines = [FabricPOItemInline]

class FabricReceiptItemInline(admin.TabularInline):
    model = FabricReceiptItem
    extra = 1
    raw_id_fields = ('fabric',)

@admin.register(FabricReceipt)
class FabricReceiptAdmin(GuardedModelAdmin):
    list_display = ('grn_no', 'po_ref', 'receipt_date')
    list_filter = ('receipt_date', 'po_ref__supplier')
    search_fields = ('grn_no', 'po_ref__po_no')
    inlines = [FabricReceiptItemInline]


