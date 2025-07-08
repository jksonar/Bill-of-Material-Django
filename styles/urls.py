from django.urls import path
from .views import StyleListView, StyleCreateView, StyleDetailView, StyleUpdateView, StyleDeleteView, \
    StyleFabricConsumptionCreateView, StyleFabricConsumptionUpdateView, StyleFabricConsumptionDeleteView, \
    StyleAccessoryConsumptionCreateView, StyleAccessoryConsumptionUpdateView, StyleAccessoryConsumptionDeleteView

app_name = 'styles'

urlpatterns = [
    path('styles/', StyleListView.as_view(), name='style_list'),
    path('styles/add/', StyleCreateView.as_view(), name='style_create'),
    path('styles/<int:pk>/detail/', StyleDetailView.as_view(), name='style_detail'),
    path('styles/<int:pk>/edit/', StyleUpdateView.as_view(), name='style_update'),
    path('styles/<int:pk>/delete/', StyleDeleteView.as_view(), name='style_delete'),

    path('styles/<int:style_pk>/fabric-consumption/add/', StyleFabricConsumptionCreateView.as_view(), name='style_fabric_consumption_create'),
    path('styles/<int:style_pk>/fabric-consumption/<int:pk>/edit/', StyleFabricConsumptionUpdateView.as_view(), name='style_fabric_consumption_update'),
    path('styles/<int:style_pk>/fabric-consumption/<int:pk>/delete/', StyleFabricConsumptionDeleteView.as_view(), name='style_fabric_consumption_delete'),

    path('styles/<int:style_pk>/accessory-consumption/add/', StyleAccessoryConsumptionCreateView.as_view(), name='style_accessory_consumption_create'),
    path('styles/<int:style_pk>/accessory-consumption/<int:pk>/edit/', StyleAccessoryConsumptionUpdateView.as_view(), name='style_accessory_consumption_update'),
    path('styles/<int:style_pk>/accessory-consumption/<int:pk>/delete/', StyleAccessoryConsumptionDeleteView.as_view(), name='style_accessory_consumption_delete'),
]