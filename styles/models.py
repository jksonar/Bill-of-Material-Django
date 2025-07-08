from django.db import models
from masters.models import Fabric, Accessory

class Style(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='style_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class StyleFabricConsumption(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    unit = models.CharField(max_length=50)

    class Meta:
        unique_together = ('style', 'fabric')

    def __str__(self):
        return f"{self.style.name} - {self.fabric.name}"

class StyleAccessoryConsumption(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    unit = models.CharField(max_length=50)

    class Meta:
        unique_together = ('style', 'accessory')

    def __str__(self):
        return f"{self.style.name} - {self.accessory.name}"

class StyleCosting(models.Model):
    style = models.OneToOneField(Style, on_delete=models.CASCADE)
    total_fabric_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_accessory_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    margin_markup = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Percentage margin/markup")

    def __str__(self):
        return f"Costing for {self.style.name}"
