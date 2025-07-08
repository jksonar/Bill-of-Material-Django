from django.contrib import admin
from .models import FabricPO, FabricPOItem, FabricReceipt, FabricReceiptItem

admin.site.register(FabricPO)
admin.site.register(FabricPOItem)
admin.site.register(FabricReceipt)
admin.site.register(FabricReceiptItem)