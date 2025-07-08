from django.db import models
from styles.models import Style, StyleFabricConsumption, StyleAccessoryConsumption
from masters.models import Fabric, Accessory

class BOMVersion(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    version_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('order', 'version_number')
        ordering = ['-created_at']

    def __str__(self):
        return f'BOM Version {self.version_number} for Order {self.order.order_no}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    order_no = models.CharField(max_length=100, unique=True)
    customer = models.CharField(max_length=255)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_no} for {self.customer}"

    def calculate_bom(self):
        # Create a new BOM version
        last_version = BOMVersion.objects.filter(order=self).order_by('-version_number').first()
        new_version_number = 1
        if last_version:
            new_version_number = last_version.version_number + 1
        bom_version = BOMVersion.objects.create(order=self, version_number=new_version_number)

        # Calculate Fabric BOM
        for sfc in self.style.stylefabricconsumption_set.all():
            required_qty = sfc.quantity * self.quantity
            BOMFabric.objects.create(
                order=self,
                fabric=sfc.fabric,
                version=bom_version,
                required_qty=required_qty,
                balance=required_qty
            )

        # Calculate Accessory BOM
        for sac in self.style.styleaccessoryconsumption_set.all():
            required_qty = sac.quantity * self.quantity
            BOMAccessory.objects.create(
                order=self,
                accessory=sac.accessory,
                version=bom_version,
                required_qty=required_qty,
                balance=required_qty
            )

class BOMFabric(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    version = models.ForeignKey(BOMVersion, on_delete=models.CASCADE, related_name='fabric_items', null=True, blank=True)
    required_qty = models.DecimalField(max_digits=10, decimal_places=4)
    issued_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('order', 'fabric', 'version')

    def __str__(self):
        return f"BOM Fabric for {self.order.order_no} - {self.fabric.name}"

class BOMAccessory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    version = models.ForeignKey(BOMVersion, on_delete=models.CASCADE, related_name='accessory_items', null=True, blank=True)
    required_qty = models.DecimalField(max_digits=10, decimal_places=4)
    issued_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('order', 'accessory', 'version')

    def __str__(self):
        return f"BOM Accessory for {self.order.order_no} - {self.accessory.name}"
