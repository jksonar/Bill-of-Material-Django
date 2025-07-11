from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

class UserRole(models.Model):
    """
    Extended user roles for the BOM system
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MERCHANDISER', 'Merchandiser'),
        ('PROCUREMENT', 'Procurement'),
        ('VIEWER', 'Viewer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VIEWER')
    department = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.assign_permissions()
    
    def assign_permissions(self):
        """
        Assign permissions based on role
        """
        # Remove user from all BOM-related groups first
        self.user.groups.clear()
        
        # Get or create role-based groups
        if self.role == 'ADMIN':
            group, created = Group.objects.get_or_create(name='BOM_Admin')
            if created:
                # Add all permissions for admin
                permissions = Permission.objects.filter(
                    content_type__app_label__in=['masters', 'styles', 'orders', 'purchase', 'reports']
                )
                group.permissions.set(permissions)
        
        elif self.role == 'MERCHANDISER':
            group, created = Group.objects.get_or_create(name='BOM_Merchandiser')
            if created:
                # Add BOM and style management permissions
                permissions = Permission.objects.filter(
                    content_type__app_label__in=['masters', 'styles', 'orders'],
                    codename__in=[
                        'add_style', 'change_style', 'view_style',
                        'add_stylefabricconsumption', 'change_stylefabricconsumption', 'view_stylefabricconsumption',
                        'add_styleaccessoryconsumption', 'change_styleaccessoryconsumption', 'view_styleaccessoryconsumption',
                        'add_stylecosting', 'change_stylecosting', 'view_stylecosting',
                        'add_order', 'change_order', 'view_order',
                        'view_fabric', 'view_accessory', 'view_color', 'view_supplier'
                    ]
                )
                group.permissions.set(permissions)
        
        elif self.role == 'PROCUREMENT':
            group, created = Group.objects.get_or_create(name='BOM_Procurement')
            if created:
                # Add PO and supplier management permissions
                permissions = Permission.objects.filter(
                    content_type__app_label__in=['purchase', 'masters'],
                    codename__in=[
                        'add_fabricpo', 'change_fabricpo', 'view_fabricpo', 'delete_fabricpo',
                        'add_accessorypo', 'change_accessorypo', 'view_accessorypo', 'delete_accessorypo',
                        'add_fabricreceipt', 'change_fabricreceipt', 'view_fabricreceipt',
                        'add_accessoryreceipt', 'change_accessoryreceipt', 'view_accessoryreceipt',
                        'add_supplier', 'change_supplier', 'view_supplier',
                        'view_fabric', 'view_accessory', 'view_order'
                    ]
                )
                group.permissions.set(permissions)
        
        elif self.role == 'VIEWER':
            group, created = Group.objects.get_or_create(name='BOM_Viewer')
            if created:
                # Add view-only permissions
                permissions = Permission.objects.filter(
                    content_type__app_label__in=['masters', 'styles', 'orders', 'purchase', 'reports'],
                    codename__startswith='view_'
                )
                group.permissions.set(permissions)
        
        # Add user to the appropriate group
        if 'group' in locals():
            self.user.groups.add(group)

class UserSession(models.Model):
    """
    Track user sessions for audit purposes
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    session_key = models.CharField(max_length=40, unique=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

class AuditLog(models.Model):
    """
    Audit log for tracking changes in the system
    """
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('VIEW', 'View'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=200)
    changes = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} {self.action} {self.object_repr} at {self.timestamp}"