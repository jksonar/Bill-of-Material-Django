from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from masters.models import Fabric, Accessory
from styles.models import Style, StyleFabricConsumption, StyleAccessoryConsumption, StyleCosting
from orders.models import Order, BOMFabric, BOMAccessory, BOMVersion
from purchase.models import FabricPO, FabricPOItem, FabricReceipt, FabricReceiptItem

class Command(BaseCommand):
    help = 'Creates default user groups and assigns permissions.'

    def handle(self, *args, **options):
        # Define roles and their permissions
        roles = {
            'Admin': {
                'permissions': 'all',
                'models': [
                    Fabric, Accessory, Style, StyleFabricConsumption, StyleAccessoryConsumption, StyleCosting,
                    Order, BOMFabric, BOMAccessory, BOMVersion, FabricPO, FabricPOItem, FabricReceipt, FabricReceiptItem
                ]
            },
            'Merchandiser': {
                'permissions': ['view', 'add', 'change'],
                'models': [
                    Style, StyleFabricConsumption, StyleAccessoryConsumption, StyleCosting,
                    Order, BOMFabric, BOMAccessory, BOMVersion
                ]
            },
            'Procurement': {
                'permissions': ['view', 'add', 'change'],
                'models': [
                    Fabric, Accessory, FabricPO, FabricPOItem, FabricReceipt, FabricReceiptItem
                ]
            },
            'Viewer': {
                'permissions': ['view'],
                'models': [
                    Fabric, Accessory, Style, StyleFabricConsumption, StyleAccessoryConsumption, StyleCosting,
                    Order, BOMFabric, BOMAccessory, BOMVersion, FabricPO, FabricPOItem, FabricReceipt, FabricReceiptItem
                ]
            },
        }

        for role_name, role_data in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created group: {role_name}'))
            else:
                self.stdout.write(f'Group {role_name} already exists.')

            # Clear existing permissions for the group to prevent duplicates on re-run
            group.permissions.clear()

            if role_data['permissions'] == 'all':
                # Assign all permissions for Admin
                for perm in Permission.objects.all():
                    group.permissions.add(perm)
            else:
                # Assign specific permissions for other roles
                for model in role_data['models']:
                    content_type = ContentType.objects.get_for_model(model)
                    for perm_type in role_data['permissions']:
                        codename = f'{perm_type}_{model._meta.model_name}'
                        try:
                            permission = Permission.objects.get(content_type=content_type, codename=codename)
                            group.permissions.add(permission)
                        except Permission.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f'Permission {codename} for {model.__name__} does not exist. Skipping.'))
            self.stdout.write(self.style.SUCCESS(f'Permissions assigned for {role_name}.'))
