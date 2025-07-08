from django.urls import path
from .views import FabricPOListView, FabricPOCreateView, FabricPODetailView, FabricPOUpdateView, FabricPODeleteView, \
    FabricPOItemCreateView, FabricPOItemUpdateView, FabricPOItemDeleteView, \
    FabricReceiptListView, FabricReceiptCreateView, FabricReceiptDetailView, FabricReceiptUpdateView, FabricReceiptDeleteView, \
    FabricReceiptItemCreateView, FabricReceiptItemUpdateView, FabricReceiptItemDeleteView

app_name = 'purchase'

urlpatterns = [
    path('fabric-pos/', FabricPOListView.as_view(), name='fabric_po_list'),
    path('fabric-pos/add/', FabricPOCreateView.as_view(), name='fabric_po_create'),
    path('fabric-pos/<int:pk>/detail/', FabricPODetailView.as_view(), name='fabric_po_detail'),
    path('fabric-pos/<int:pk>/edit/', FabricPOUpdateView.as_view(), name='fabric_po_update'),
    path('fabric-pos/<int:pk>/delete/', FabricPODeleteView.as_view(), name='fabric_po_delete'),

    path('fabric-pos/<int:po_pk>/items/add/', FabricPOItemCreateView.as_view(), name='fabric_po_item_create'),
    path('fabric-pos/<int:po_pk>/items/<int:pk>/edit/', FabricPOItemUpdateView.as_view(), name='fabric_po_item_update'),
    path('fabric-pos/<int:po_pk>/items/<int:pk>/delete/', FabricPOItemDeleteView.as_view(), name='fabric_po_item_delete'),

    path('fabric-receipts/', FabricReceiptListView.as_view(), name='fabric_receipt_list'),
    path('fabric-receipts/add/', FabricReceiptCreateView.as_view(), name='fabric_receipt_create'),
    path('fabric-receipts/<int:pk>/detail/', FabricReceiptDetailView.as_view(), name='fabric_receipt_detail'),
    path('fabric-receipts/<int:pk>/edit/', FabricReceiptUpdateView.as_view(), name='fabric_receipt_update'),
    path('fabric-receipts/<int:pk>/delete/', FabricReceiptDeleteView.as_view(), name='fabric_receipt_delete'),

    path('fabric-receipts/<int:receipt_pk>/items/add/', FabricReceiptItemCreateView.as_view(), name='fabric_receipt_item_create'),
    path('fabric-receipts/<int:receipt_pk>/items/<int:pk>/edit/', FabricReceiptItemUpdateView.as_view(), name='fabric_receipt_item_update'),
    path('fabric-receipts/<int:receipt_pk>/items/<int:pk>/delete/', FabricReceiptItemDeleteView.as_view(), name='fabric_receipt_item_delete'),
]