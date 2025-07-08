from django.db import models
from styles.models import Style
from masters.models import Fabric, Accessory

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

class BOMFabric(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    required_qty = models.DecimalField(max_digits=10, decimal_places=4)
    issued_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('order', 'fabric')

    def __str__(self):
        return f"BOM Fabric for {self.order.order_no} - {self.fabric.name}"

class BOMAccessory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    required_qty = models.DecimalField(max_digits=10, decimal_places=4)
    issued_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('order', 'accessory')

    def __str__(self):
        return f"BOM Accessory for {self.order.order_no} - {self.accessory.name}"
