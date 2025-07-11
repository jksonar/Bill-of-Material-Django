from django.db import models
from masters.models import Fabric, Accessory, Color

class Currency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Style(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    item_description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='style_images/', blank=True, null=True)
    sizes = models.ManyToManyField(Size, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    associated_styles = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name

class StyleVariant(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('style', 'size', 'color')

    def __str__(self):
        return f'{self.style.name} - {self.size.name} - {self.color.name}'

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
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000)
    total_fabric_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_accessory_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    margin_markup = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Percentage margin/markup")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Percentage discount")
    landed_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Costing for {self.style.name}"

    def calculate_costs(self):
        total_fabric_cost = sum(f.quantity * f.fabric.unit_price for f in self.style.stylefabricconsumption_set.all())
        total_accessory_cost = sum(a.quantity * a.accessory.price for a in self.style.styleaccessoryconsumption_set.all())
        self.total_fabric_cost = total_fabric_cost * self.exchange_rate
        self.total_accessory_cost = total_accessory_cost * self.exchange_rate
        self.total_cost = (total_fabric_cost + total_accessory_cost) * self.exchange_rate
        self.landed_cost = self.total_cost * (1 + self.margin_markup / 100)
        self.retail_price = self.landed_cost * (1 - self.discount / 100)
        self.save()
