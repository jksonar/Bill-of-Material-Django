from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserRole, UserSession, AuditLog

class UserRoleInline(admin.StackedInline):
    model = UserRole
    can_delete = False
    verbose_name_plural = 'User Role'

class UserAdmin(BaseUserAdmin):
    inlines = (UserRoleInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'userrole__role')
    
    def get_role(self, obj):
        try:
            return obj.userrole.get_role_display()
        except UserRole.DoesNotExist:
            return 'No Role'
    get_role.short_description = 'Role'
    get_role.admin_order_field = 'userrole__role'

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'employee_id', 'is_active', 'created_at')
    list_filter = ('role', 'department', 'is_active', 'created_at')
    search_fields = ('user__username', 'user__email', 'employee_id', 'department')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Additional Details', {
            'fields': ('department', 'employee_id', 'phone', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time', 'ip_address', 'session_duration')
    list_filter = ('login_time', 'logout_time')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('login_time', 'logout_time', 'session_key')
    
    def session_duration(self, obj):
        if obj.logout_time:
            duration = obj.logout_time - obj.login_time
            return str(duration)
        return 'Active'
    session_duration.short_description = 'Duration'

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'content_type', 'object_repr', 'timestamp')
    list_filter = ('action', 'content_type', 'timestamp')
    search_fields = ('user__username', 'object_repr')
    readonly_fields = ('user', 'action', 'content_type', 'object_id', 'object_repr', 'changes', 'timestamp', 'ip_address')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)