from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FabricReceiptItem
from masters.models import Inventory

@receiver(post_save, sender=FabricReceiptItem)
def update_inventory_on_fabric_receipt(sender, instance, created, **kwargs):
    if created:
        inventory, _ = Inventory.objects.get_or_create(fabric=instance.fabric)
        inventory.quantity += instance.quantity_received
        inventory.save()
