from django.db import models
from masters.models import Fabric, Color

class FabricPO(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Received', 'Received'),
        ('Cancelled', 'Cancelled'),
    ]

    po_no = models.CharField(max_length=100, unique=True)
    supplier = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    total_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    shipping_address = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')

    def __str__(self):
        return f"PO {self.po_no} from {self.supplier}"

class FabricPOItem(models.Model):
    po = models.ForeignKey(FabricPO, on_delete=models.CASCADE, related_name='items')
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('po', 'fabric', 'color')

    def __str__(self):
        return f"{self.fabric.name} ({self.color.name}) - {self.quantity} @ {self.rate}"

class FabricReceipt(models.Model):
    po_ref = models.ForeignKey(FabricPO, on_delete=models.CASCADE)
    receipt_date = models.DateField(auto_now_add=True)
    grn_no = models.CharField(max_length=100, unique=True, verbose_name="GRN No")

    def __str__(self):
        return f"Receipt {self.grn_no} for PO {self.po_ref.po_no}"

class FabricReceiptItem(models.Model):
    receipt = models.ForeignKey(FabricReceipt, on_delete=models.CASCADE, related_name='items')
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=4)
    damage_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)

    def __str__(self):
        return f"{self.fabric.name} ({self.color.name}) - {self.quantity_received} received"
