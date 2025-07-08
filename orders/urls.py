from django.urls import path
from .views import OrderListView, OrderDetailView, OrderUpdateView, BOMFabricUpdateView, BOMAccessoryUpdateView, BOMSummaryView

app_name = 'orders'

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/detail/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/edit/', OrderUpdateView.as_view(), name='order_update'),
    path('bom-fabric/<int:pk>/edit/', BOMFabricUpdateView.as_view(), name='bom_fabric_update'),
    path('bom-accessory/<int:pk>/edit/', BOMAccessoryUpdateView.as_view(), name='bom_accessory_update'),
    path('bom-summary/', BOMSummaryView.as_view(), name='bom_summary'),
]