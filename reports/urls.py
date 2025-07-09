from django.urls import path
from .views import BOMReportView, PurchaseOrderReportView, PurchaseReceiptReportView, BOMDiffView, StyleCostingReportView

app_name = 'reports'

urlpatterns = [
    path('bom-report/', BOMReportView.as_view(), name='bom_report'),
    path('purchase-order-report/', PurchaseOrderReportView.as_view(), name='purchase_order_report'),
    path('purchase-receipt-report/', PurchaseReceiptReportView.as_view(), name='purchase_receipt_report'),
    path('bom-diff/', BOMDiffView.as_view(), name='bom_diff'),
    path('style-costing-report/', StyleCostingReportView.as_view(), name='style_costing_report'),
]