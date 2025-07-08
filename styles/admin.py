from django.contrib import admin
from .models import Style, StyleFabricConsumption, StyleAccessoryConsumption, StyleCosting, Size, StyleVariant, Currency

class StyleFabricConsumptionInline(admin.TabularInline):
    model = StyleFabricConsumption
    extra = 1
    raw_id_fields = ('fabric',)

class StyleAccessoryConsumptionInline(admin.TabularInline):
    model = StyleAccessoryConsumption
    extra = 1
    raw_id_fields = ('accessory',)

class StyleVariantInline(admin.TabularInline):
    model = StyleVariant
    extra = 1

@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'image')
    search_fields = ('code', 'name', 'category')
    list_filter = ('category',)
    inlines = [StyleVariantInline, StyleFabricConsumptionInline, StyleAccessoryConsumptionInline]

@admin.register(StyleCosting)
class StyleCostingAdmin(admin.ModelAdmin):
    list_display = ('style', 'currency', 'exchange_rate', 'total_fabric_cost', 'total_accessory_cost', 'total_cost', 'margin_markup', 'discount', 'landed_cost', 'retail_price')
    readonly_fields = ('total_fabric_cost', 'total_accessory_cost', 'total_cost', 'landed_cost', 'retail_price')

admin.site.register(Size)
admin.site.register(Currency)
