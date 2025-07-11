from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import FabricPO, FabricPOItem, FabricReceipt, FabricReceiptItem
from django.db.models import Q

class FabricPOListView(LoginRequiredMixin, ListView):
    model = FabricPO
    template_name = 'purchase/fabric_po_list.html'
    context_object_name = 'fabric_pos'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_statuses'] = FabricPO.STATUS_CHOICES
        context['selected_status'] = self.request.GET.get('status', '')
        return context

class FabricPOCreateView(LoginRequiredMixin, CreateView):
    model = FabricPO
    template_name = 'purchase/fabric_po_form.html'
    fields = ['po_no', 'supplier', 'delivery_date', 'status']
    success_url = reverse_lazy('purchase:fabric_po_list')

class FabricPODetailView(LoginRequiredMixin, DetailView):
    model = FabricPO
    template_name = 'purchase/fabric_po_detail.html'
    context_object_name = 'fabric_po'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = FabricPOItem.objects.filter(po=self.object)
        return context

class FabricPOUpdateView(LoginRequiredMixin, UpdateView):
    model = FabricPO
    template_name = 'purchase/fabric_po_form.html'
    fields = ['po_no', 'supplier', 'delivery_date', 'status']
    success_url = reverse_lazy('purchase:fabric_po_list')

class FabricPODeleteView(LoginRequiredMixin, DeleteView):
    model = FabricPO
    template_name = 'purchase/fabric_po_confirm_delete.html'
    success_url = reverse_lazy('purchase:fabric_po_list')


class FabricPOItemCreateView(LoginRequiredMixin, CreateView):
    model = FabricPOItem
    template_name = 'purchase/fabric_po_item_form.html'
    fields = ['fabric', 'quantity', 'rate']

    def form_valid(self, form):
        form.instance.po = FabricPO.objects.get(pk=self.kwargs['po_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('purchase:fabric_po_detail', kwargs={'pk': self.kwargs['po_pk']})

class FabricPOItemUpdateView(LoginRequiredMixin, UpdateView):
    model = FabricPOItem
    template_name = 'purchase/fabric_po_item_form.html'
    fields = ['fabric', 'quantity', 'rate']

    def get_success_url(self):
        return reverse_lazy('purchase:fabric_po_detail', kwargs={'pk': self.kwargs['po_pk']})

class FabricPOItemDeleteView(LoginRequiredMixin, DeleteView):
    model = FabricPOItem
    template_name = 'purchase/fabric_po_item_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('purchase:fabric_po_detail', kwargs={'pk': self.kwargs['po_pk']})


class FabricReceiptListView(LoginRequiredMixin, ListView):
    model = FabricReceipt
    template_name = 'purchase/fabric_receipt_list.html'
    context_object_name = 'fabric_receipts'

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            queryset = queryset.filter(receipt_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(receipt_date__lte=end_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context

class FabricReceiptCreateView(LoginRequiredMixin, CreateView):
    model = FabricReceipt
    template_name = 'purchase/fabric_receipt_form.html'
    fields = ['po_ref', 'grn_no']
    success_url = reverse_lazy('purchase:fabric_receipt_list')

class FabricReceiptDetailView(LoginRequiredMixin, DetailView):
    model = FabricReceipt
    template_name = 'purchase/fabric_receipt_detail.html'
    context_object_name = 'fabric_receipt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = FabricReceiptItem.objects.filter(receipt=self.object)
        return context

class FabricReceiptUpdateView(LoginRequiredMixin, UpdateView):
    model = FabricReceipt
    template_name = 'purchase/fabric_receipt_form.html'
    fields = ['po_ref', 'grn_no']
    success_url = reverse_lazy('purchase:fabric_receipt_list')

class FabricReceiptDeleteView(LoginRequiredMixin, DeleteView):
    model = FabricReceipt
    template_name = 'purchase/fabric_receipt_confirm_delete.html'
    success_url = reverse_lazy('purchase:fabric_receipt_list')


class FabricReceiptItemCreateView(LoginRequiredMixin, CreateView):
    model = FabricReceiptItem
    template_name = 'purchase/fabric_receipt_item_form.html'
    fields = ['fabric', 'quantity_received', 'damage_qty']

    def form_valid(self, form):
        form.instance.receipt = FabricReceipt.objects.get(pk=self.kwargs['receipt_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('purchase:fabric_receipt_detail', kwargs={'pk': self.kwargs['receipt_pk']})

class FabricReceiptItemUpdateView(LoginRequiredMixin, UpdateView):
    model = FabricReceiptItem
    template_name = 'purchase/fabric_receipt_item_form.html'
    fields = ['fabric', 'quantity_received', 'damage_qty']

    def get_success_url(self):
        return reverse_lazy('purchase:fabric_receipt_detail', kwargs={'pk': self.kwargs['receipt_pk']})

class FabricReceiptItemDeleteView(LoginRequiredMixin, DeleteView):
    model = FabricReceiptItem
    template_name = 'purchase/fabric_receipt_item_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('purchase:fabric_receipt_detail', kwargs={'pk': self.kwargs['receipt_pk']})