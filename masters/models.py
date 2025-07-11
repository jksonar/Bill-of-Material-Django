from django.db import models
from django.contrib.auth.models import User

class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, blank=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    lead_time_days = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_supplier = Supplier.objects.all().order_by('id').last()
            if last_supplier:
                last_id = last_supplier.id
            else:
                last_id = 0
            self.code = f'SUP-{last_id + 1:06d}'
        super(Supplier, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True, help_text="Hex color code (e.g., #FF0000)")

    def __str__(self):
        return self.name

class Fabric(models.Model):
    UNIT_CHOICES = [
        ('MTR', 'Meter'),
        ('YRD', 'Yard'),
        ('KG', 'Kilogram'),
        ('LB', 'Pound'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    construction = models.CharField(max_length=255, blank=True, null=True)
    composition = models.CharField(max_length=255, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    stock_in_hand = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Width in inches")
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Weight in GSM")
    lead_time = models.IntegerField(blank=True, null=True, help_text="Lead time in days")
    image = models.ImageField(upload_to='fabric_images/', blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='MTR')
    minimum_order_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_fabric = Fabric.objects.all().order_by('id').last()
            if last_fabric:
                last_id = last_fabric.id
            else:
                last_id = 0
            self.code = f'F-{last_id + 1:06d}'
        super(Fabric, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class FabricColor(models.Model):
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    stock = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    po_quantity = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)

    class Meta:
        unique_together = ('fabric', 'color')

    def __str__(self):
        return f'{self.fabric.name} - {self.color.name}'

class Accessory(models.Model):
    UNIT_CHOICES = [
        ('PCS', 'Pieces'),
        ('SET', 'Set'),
        ('PAIR', 'Pair'),
        ('MTR', 'Meter'),
        ('YRD', 'Yard'),
        ('KG', 'Kilogram'),
        ('GRAM', 'Gram'),
    ]
    
    CATEGORY_CHOICES = [
        ('BUTTON', 'Button'),
        ('ZIPPER', 'Zipper'),
        ('THREAD', 'Thread'),
        ('LABEL', 'Label'),
        ('TRIM', 'Trim'),
        ('PACKAGING', 'Packaging'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    finish = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    weight = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='PCS')
    lead_time = models.IntegerField(blank=True, null=True, help_text="Lead time in days")
    stock = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    minimum_order_qty = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    image = models.ImageField(upload_to='accessory_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_accessory = Accessory.objects.all().order_by('id').last()
            if last_accessory:
                last_id = last_accessory.id
            else:
                last_id = 0
            self.code = f'A-{last_id + 1:06d}'
        super(Accessory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class AccessoryColor(models.Model):
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    stock = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    po_quantity = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)

    class Meta:
        unique_together = ('accessory', 'color')

    def __str__(self):
        return f'{self.accessory.name} - {self.color.name}'

