from django.urls import path
from .views import FabricListView, FabricCreateView, FabricDetailView, FabricUpdateView, FabricDeleteView,     AccessoryListView, AccessoryCreateView, AccessoryDetailView, AccessoryUpdateView, AccessoryDeleteView

app_name = 'masters'

urlpatterns = [
    path('fabrics/', FabricListView.as_view(), name='fabric_list'),
    path('fabrics/add/', FabricCreateView.as_view(), name='fabric_create'),
    path('fabrics/<int:pk>/detail/', FabricDetailView.as_view(), name='fabric_detail'),
    path('fabrics/<int:pk>/edit/', FabricUpdateView.as_view(), name='fabric_update'),
    path('fabrics/<int:pk>/delete/', FabricDeleteView.as_view(), name='fabric_delete'),

    path('accessories/', AccessoryListView.as_view(), name='accessory_list'),
    path('accessories/add/', AccessoryCreateView.as_view(), name='accessory_create'),
    path('accessories/<int:pk>/detail/', AccessoryDetailView.as_view(), name='accessory_detail'),
    path('accessories/<int:pk>/edit/', AccessoryUpdateView.as_view(), name='accessory_update'),
    path('accessories/<int:pk>/delete/', AccessoryDeleteView.as_view(), name='accessory_delete'),
]