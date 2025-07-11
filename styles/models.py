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
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    wastage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, help_text="Wastage percentage")
    unit = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('style', 'fabric', 'size', 'color')

    def __str__(self):
        size_color = ""
        if self.size:
            size_color += f" - {self.size.name}"
        if self.color:
            size_color += f" - {self.color.name}"
        return f"{self.style.name} - {self.fabric.name}{size_color}"
    
    def get_total_consumption(self):
        """Calculate total consumption including wastage"""
        return self.quantity * (1 + self.wastage_percentage / 100)

class StyleAccessoryConsumption(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    wastage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=2.00, help_text="Wastage percentage")
    unit = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('style', 'accessory', 'size', 'color')

    def __str__(self):
        size_color = ""
        if self.size:
            size_color += f" - {self.size.name}"
        if self.color:
            size_color += f" - {self.color.name}"
        return f"{self.style.name} - {self.accessory.name}{size_color}"
    
    def get_total_consumption(self):
        """Calculate total consumption including wastage"""
        return self.quantity * (1 + self.wastage_percentage / 100)

class StyleCosting(models.Model):
    style = models.OneToOneField(Style, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000)
    
    # Material Costs
    total_fabric_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    total_accessory_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    material_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    
    # Additional Costs
    production_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.00, help_text="Production/Manufacturing cost")
    overhead_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.00, help_text="Overhead cost")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.00, help_text="Shipping/Freight cost")
    other_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.00, help_text="Other miscellaneous costs")
    
    # Total and Pricing
    total_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    margin_markup = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Percentage margin/markup")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Percentage discount")
    landed_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    retail_price = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    
    # Metadata
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Costing for {self.style.name}"

    def calculate_costs(self):
        """Calculate all costs based on consumption and pricing"""
        # Filter consumption based on size/color if specified
        fabric_consumptions = self.style.stylefabricconsumption_set.all()
        accessory_consumptions = self.style.styleaccessoryconsumption_set.all()
        
        if self.size:
            fabric_consumptions = fabric_consumptions.filter(models.Q(size=self.size) | models.Q(size__isnull=True))
            accessory_consumptions = accessory_consumptions.filter(models.Q(size=self.size) | models.Q(size__isnull=True))
        
        if self.color:
            fabric_consumptions = fabric_consumptions.filter(models.Q(color=self.color) | models.Q(color__isnull=True))
            accessory_consumptions = accessory_consumptions.filter(models.Q(color=self.color) | models.Q(color__isnull=True))
        
        # Calculate fabric costs with wastage
        total_fabric_cost = sum(f.get_total_consumption() * f.fabric.unit_price for f in fabric_consumptions)
        
        # Calculate accessory costs with wastage
        total_accessory_cost = sum(a.get_total_consumption() * a.accessory.price for a in accessory_consumptions)
        
        # Apply exchange rate
        self.total_fabric_cost = total_fabric_cost * self.exchange_rate
        self.total_accessory_cost = total_accessory_cost * self.exchange_rate
        self.material_cost = self.total_fabric_cost + self.total_accessory_cost
        
        # Calculate total cost including all additional costs
        self.total_cost = (self.material_cost + self.production_cost + 
                          self.overhead_cost + self.shipping_cost + self.other_cost)
        
        # Calculate landed cost with markup
        self.landed_cost = self.total_cost * (1 + self.margin_markup / 100)
        
        # Calculate retail price with discount
        self.retail_price = self.landed_cost * (1 - self.discount / 100)
        
        self.save()
