from django.db import models
from masters.models import Fabric, Accessory, Color, Supplier
from orders.models import Order

class FabricPO(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('OPEN', 'Open'),
        ('PARTIAL', 'Partially Received'),
        ('RECEIVED', 'Fully Received'),
        ('CANCELLED', 'Cancelled'),
    ]

    po_no = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, help_text="Related order if any")
    date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    total_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=4, default=0.00)
    shipping_address = models.TextField(blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

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
    rate_received = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    inspection_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fabric.name} ({self.color.name}) - {self.quantity_received} received"

# Accessory Purchase Models
class AccessoryPO(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('OPEN', 'Open'),
        ('PARTIAL', 'Partially Received'),
        ('RECEIVED', 'Fully Received'),
        ('CANCELLED', 'Cancelled'),
    ]

    po_no = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, help_text="Related order if any")
    date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    total_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=4, default=0.00)
    shipping_address = models.TextField(blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Accessory PO {self.po_no} from {self.supplier.name}"

class AccessoryPOItem(models.Model):
    po = models.ForeignKey(AccessoryPO, on_delete=models.CASCADE, related_name='items')
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    total_amount = models.DecimalField(max_digits=12, decimal_places=4, default=0.00)

    class Meta:
        unique_together = ('po', 'accessory', 'color')

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.rate
        super().save(*args, **kwargs)

    def __str__(self):
        color_str = f" ({self.color.name})" if self.color else ""
        return f"{self.accessory.name}{color_str} - {self.quantity} @ {self.rate}"

class AccessoryReceipt(models.Model):
    po_ref = models.ForeignKey(AccessoryPO, on_delete=models.CASCADE)
    receipt_date = models.DateField(auto_now_add=True)
    grn_no = models.CharField(max_length=100, unique=True, verbose_name="GRN No")
    received_by = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Accessory Receipt {self.grn_no} for PO {self.po_ref.po_no}"

class AccessoryReceiptItem(models.Model):
    receipt = models.ForeignKey(AccessoryReceipt, on_delete=models.CASCADE, related_name='items')
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=4)
    damage_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    rate_received = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    inspection_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        color_str = f" ({self.color.name})" if self.color else ""
        return f"{self.accessory.name}{color_str} - {self.quantity_received} received"
