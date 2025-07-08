from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Fabric, Accessory
from django.db import models

class FabricListView(ListView):
    model = Fabric
    template_name = 'masters/fabric_list.html'
    context_object_name = 'fabrics'

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

class FabricCreateView(CreateView):
    model = Fabric
    template_name = 'masters/fabric_form.html'
    fields = ['name', 'code', 'type', 'gsm', 'width', 'supplier', 'notes']
    success_url = reverse_lazy('masters:fabric_list')

class FabricDetailView(DetailView):
    model = Fabric
    template_name = 'masters/fabric_detail.html'
    context_object_name = 'fabric'

class FabricUpdateView(UpdateView):
    model = Fabric
    template_name = 'masters/fabric_form.html'
    fields = ['name', 'code', 'type', 'gsm', 'width', 'supplier', 'notes']
    success_url = reverse_lazy('masters:fabric_list')

class FabricDeleteView(DeleteView):
    model = Fabric
    template_name = 'masters/fabric_confirm_delete.html'
    success_url = reverse_lazy('masters:fabric_list')


class AccessoryListView(ListView):
    model = Accessory
    template_name = 'masters/accessory_list.html'
    context_object_name = 'accessories'

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

class AccessoryCreateView(CreateView):
    model = Accessory
    template_name = 'masters/accessory_form.html'
    fields = ['name', 'code', 'type', 'supplier', 'usage_notes']
    success_url = reverse_lazy('masters:accessory_list')

class AccessoryDetailView(DetailView):
    model = Accessory
    template_name = 'masters/accessory_detail.html'
    context_object_name = 'accessory'

class AccessoryUpdateView(UpdateView):
    model = Accessory
    template_name = 'masters/accessory_form.html'
    fields = ['name', 'code', 'type', 'supplier', 'usage_notes']
    success_url = reverse_lazy('masters:accessory_list')

class AccessoryDeleteView(DeleteView):
    model = Accessory
    template_name = 'masters/accessory_confirm_delete.html'
    success_url = reverse_lazy('masters:accessory_list')