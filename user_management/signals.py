from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserRole

@receiver(post_save, sender=User)
def create_or_update_user_role(sender, instance, created, **kwargs):
    user_role, created = UserRole.objects.get_or_create(user=instance)
    # Directly call assign_permissions on the user_role object
    user_role.assign_permissions()