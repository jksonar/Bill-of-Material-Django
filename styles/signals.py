from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Style, StyleFabricConsumption, StyleAccessoryConsumption, StyleCosting

@receiver(post_save, sender=Style)
def create_or_update_style_costing(sender, instance, created, **kwargs):
    if created:
        StyleCosting.objects.create(style=instance)
    instance.stylecosting.calculate_costs()

@receiver(post_save, sender=StyleFabricConsumption)
@receiver(post_save, sender=StyleAccessoryConsumption)
def update_style_costing_on_consumption_change(sender, instance, **kwargs):
    instance.style.stylecosting.calculate_costs()
