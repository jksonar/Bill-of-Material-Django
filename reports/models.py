from django.db import models
from django.contrib.auth.models import User
from styles.models import Style
from orders.models import Order
from purchase.models import FabricPO, AccessoryPO

class ReportTemplate(models.Model):
    REPORT_TYPES = [
        ('BOM', 'Bill of Materials'),
        ('COSTING', 'Style Costing'),
        ('PO', 'Purchase Order'),
        ('RECEIPT', 'Material Receipt'),
        ('INVENTORY', 'Inventory Report'),
        ('ORDER_SUMMARY', 'Order Summary'),
    ]
    
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True, null=True)
    template_content = models.TextField(help_text="HTML template content")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_report_type_display()})"

class ReportGeneration(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    FORMAT_CHOICES = [
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
        ('CSV', 'CSV'),
    ]
    
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='PDF')
    parameters = models.JSONField(default=dict, help_text="Report parameters as JSON")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    file_path = models.CharField(max_length=500, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.template.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class BOMReport(models.Model):
    """Model to store BOM report data for quick access"""
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    version = models.IntegerField(default=1)
    total_fabric_cost = models.DecimalField(max_digits=12, decimal_places=4, default=0.00)
    total_accessory_cost = models.DecimalField(max_digits=12, decimal_places=4, default=0.00)
    total_cost = models.DecimalField(max_digits=12, decimal_places=4, default=0.00)
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ('style', 'order', 'version')
    
    def __str__(self):
        order_str = f" for Order {self.order.order_no}" if self.order else ""
        return f"BOM Report for {self.style.name}{order_str} v{self.version}"
