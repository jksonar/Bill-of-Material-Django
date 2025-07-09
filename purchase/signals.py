from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FabricReceiptItem
from masters.models import FabricColor, Fabric
from django.db.models import Sum

@receiver(post_save, sender=FabricReceiptItem)
def update_inventory_on_fabric_receipt(sender, instance, created, **kwargs):
    if created and instance.color:
        # Update the stock for the specific color
        fabric_color, _ = FabricColor.objects.get_or_create(
            fabric=instance.fabric,
            color=instance.color
        )
        fabric_color.stock += instance.quantity_received - instance.damage_qty
        fabric_color.save()

        # Update the total stock in hand for the fabric
        total_stock = FabricColor.objects.filter(fabric=instance.fabric).aggregate(total=Sum('stock'))['total']
        instance.fabric.stock_in_hand = total_stock or 0
        instance.fabric.save()
