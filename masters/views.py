from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Fabric, Accessory
from django.db import models
from django.contrib.auth.mixins import PermissionRequiredMixin

class FabricListView(PermissionRequiredMixin, ListView):
    model = Fabric
    template_name = 'masters/fabric_list.html'
    context_object_name = 'fabrics'
    permission_required = 'masters.view_fabric'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        fabric_type = self.request.GET.get('type')
        supplier = self.request.GET.get('supplier')

        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) |
                models.Q(code__icontains=query) |
                models.Q(supplier__icontains=query)
            )
        if fabric_type:
            queryset = queryset.filter(type__icontains=fabric_type)
        if supplier:
            queryset = queryset.filter(supplier__icontains=supplier)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['selected_supplier'] = self.request.GET.get('supplier', '')
        context['all_types'] = Fabric.objects.values_list('type', flat=True).distinct().exclude(type__isnull=True).exclude(type__exact='')
        context['all_suppliers'] = Fabric.objects.values_list('supplier', flat=True).distinct().exclude(supplier__isnull=True).exclude(supplier__exact='')
        return context

class FabricCreateView(PermissionRequiredMixin, CreateView):
    model = Fabric
    template_name = 'masters/fabric_form.html'
    fields = ['name', 'code', 'type', 'gsm', 'width', 'supplier', 'notes']
    success_url = reverse_lazy('masters:fabric_list')
    permission_required = 'masters.add_fabric'

class FabricDetailView(PermissionRequiredMixin, DetailView):
    model = Fabric
    template_name = 'masters/fabric_detail.html'
    context_object_name = 'fabric'
    permission_required = 'masters.view_fabric'

class FabricUpdateView(PermissionRequiredMixin, UpdateView):
    model = Fabric
    template_name = 'masters/fabric_form.html'
    fields = ['name', 'code', 'type', 'gsm', 'width', 'supplier', 'notes']
    success_url = reverse_lazy('masters:fabric_list')
    permission_required = 'masters.change_fabric'

class FabricDeleteView(PermissionRequiredMixin, DeleteView):
    model = Fabric
    template_name = 'masters/fabric_confirm_delete.html'
    success_url = reverse_lazy('masters:fabric_list')
    permission_required = 'masters.delete_fabric'


class AccessoryListView(PermissionRequiredMixin, ListView):
    model = Accessory
    template_name = 'masters/accessory_list.html'
    context_object_name = 'accessories'
    permission_required = 'masters.view_accessory'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        accessory_type = self.request.GET.get('type')
        supplier = self.request.GET.get('supplier')

        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) |
                models.Q(code__icontains=query) |
                models.Q(supplier__icontains=query)
            )
        if accessory_type:
            queryset = queryset.filter(type__icontains=accessory_type)
        if supplier:
            queryset = queryset.filter(supplier__icontains=supplier)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['selected_supplier'] = self.request.GET.get('supplier', '')
        context['all_types'] = Accessory.objects.values_list('type', flat=True).distinct().exclude(type__isnull=True).exclude(type__exact='')
        context['all_suppliers'] = Accessory.objects.values_list('supplier', flat=True).distinct().exclude(supplier__isnull=True).exclude(supplier__exact='')
        return context

class AccessoryCreateView(PermissionRequiredMixin, CreateView):
    model = Accessory
    template_name = 'masters/accessory_form.html'
    fields = ['name', 'code', 'type', 'supplier', 'usage_notes']
    success_url = reverse_lazy('masters:accessory_list')
    permission_required = 'masters.add_accessory'

class AccessoryDetailView(PermissionRequiredMixin, DetailView):
    model = Accessory
    template_name = 'masters/accessory_detail.html'
    context_object_name = 'accessory'
    permission_required = 'masters.view_accessory'

class AccessoryUpdateView(PermissionRequiredMixin, UpdateView):
    model = Accessory
    template_name = 'masters/accessory_form.html'
    fields = ['name', 'code', 'type', 'supplier', 'usage_notes']
    success_url = reverse_lazy('masters:accessory_list')
    permission_required = 'masters.change_accessory'

class AccessoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = Accessory
    template_name = 'masters/accessory_confirm_delete.html'
    success_url = reverse_lazy('masters:accessory_list')
    permission_required = 'masters.delete_accessory'