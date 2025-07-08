from django.contrib import admin
from .models import Style, StyleFabricConsumption, StyleAccessoryConsumption, StyleCosting

admin.site.register(Style)
admin.site.register(StyleFabricConsumption)
admin.site.register(StyleAccessoryConsumption)
admin.site.register(StyleCosting)
