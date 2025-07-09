from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Fabric(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    construction = models.CharField(max_length=255, blank=True, null=True)
    composition = models.CharField(max_length=255, blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    stock_in_hand = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    lead_time = models.IntegerField(blank=True, null=True) # in days
    image = models.ImageField(upload_to='fabric_images/', blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

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
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    finish = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    lead_time = models.IntegerField(blank=True, null=True) # in days
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='accessory_images/', blank=True, null=True)

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

