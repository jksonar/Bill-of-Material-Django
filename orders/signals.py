from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def create_or_update_bom(sender, instance, created, **kwargs):
    if created or instance.pk is not None: # Ensure BOM is calculated on creation and subsequent updates
        instance.calculate_bom()