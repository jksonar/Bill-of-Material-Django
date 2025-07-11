from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Fabric, Accessory
from django.db import models
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse

class FabricListView(PermissionRequiredMixin, ListView):
    model = Fabric
    template_name = 'masters/fabric_list.html'
    context_object_name = 'fabrics'
    permission_required = 'masters.view_fabric'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        fabric_construction = self.request.GET.get('construction')
        supplier = self.request.GET.get('supplier')

        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) |
                models.Q(code__icontains=query) |
                models.Q(supplier__name__icontains=query)
            )
        if fabric_construction:
            queryset = queryset.filter(construction__icontains=fabric_construction)
        if supplier:
            queryset = queryset.filter(supplier__name__icontains=supplier)
        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return ['masters/partials/fabric_list_partial.html']
        return ['masters/fabric_list.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['selected_construction'] = self.request.GET.get('construction', '')
        context['selected_supplier'] = self.request.GET.get('supplier', '')
        context['all_constructions'] = Fabric.objects.values_list('construction', flat=True).distinct().exclude(construction__isnull=True).exclude(construction__exact='')
        context['all_suppliers'] = Fabric.objects.values_list('supplier__name', flat=True).distinct().exclude(supplier__isnull=True).exclude(supplier__name__exact='')
        return context

class FabricCreateView(PermissionRequiredMixin, CreateView):
    model = Fabric
    template_name = 'masters/fabric_form.html'
    fields = ['name', 'code', 'description', 'construction', 'composition', 'supplier', 'width', 'weight', 'lead_time', 'unit_price', 'image']
    success_url = reverse_lazy('masters:fabric_list')
    permission_required = 'masters.add_fabric'

    def get_template_names(self):
        if self.request.htmx:
            return ['masters/partials/fabric_form_partial.html']
        return ['masters/fabric_form.html']

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx:
            messages.success(self.request, "Fabric created successfully!")
            self.object.refresh_from_db()
            return render(self.request, 'masters/partials/fabric_detail_partial.html', {'fabric': self.object})
        return response

class FabricDetailView(PermissionRequiredMixin, DetailView):
    model = Fabric
    template_name = 'masters/fabric_detail.html'
    context_object_name = 'fabric'
    permission_required = 'masters.view_fabric'

    def get_template_names(self):
        if self.request.htmx:
            return ['masters/partials/fabric_detail_partial.html']
        return ['masters/fabric_detail.html']

class FabricUpdateView(PermissionRequiredMixin, UpdateView):
    model = Fabric
    template_name = 'masters/fabric_form.html'
    fields = ['name', 'code', 'description', 'construction', 'composition', 'supplier', 'width', 'weight', 'lead_time', 'unit_price', 'image']
    success_url = reverse_lazy('masters:fabric_list')
    permission_required = 'masters.change_fabric'

    def get_template_names(self):
        if self.request.htmx:
            return ['masters/partials/fabric_form_partial.html']
        return ['masters/fabric_form.html']

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx:
            messages.success(self.request, "Fabric updated successfully!")
            self.object.refresh_from_db()
            return render(self.request, 'masters/partials/fabric_detail_partial.html', {'fabric': self.object})
        return response

class FabricDeleteView(PermissionRequiredMixin, DeleteView):
    model = Fabric
    template_name = 'masters/fabric_confirm_delete.html'
    success_url = reverse_lazy('masters:fabric_list')
    permission_required = 'masters.delete_fabric'

    def get_template_names(self):
        if self.request.htmx:
            return ['masters/partials/fabric_confirm_delete_partial.html']
        return ['masters/fabric_confirm_delete.html']

    def form_valid(self, form):
        if self.request.htmx:
            self.object.delete()
            messages.success(self.request, "Fabric deleted successfully!")
            return HttpResponse(status=204, headers={'HX-Redirect': self.success_url})
        return super().form_valid(form)


class AccessoryListView(PermissionRequiredMixin, ListView):
    model = Accessory
    template_name = 'masters/accessory_list.html'
    context_object_name = 'accessories'
    permission_required = 'masters.view_accessory'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        accessory_finish = self.request.GET.get('finish')
        supplier = self.request.GET.get('supplier')

        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) |
                models.Q(code__icontains=query) |
                models.Q(supplier__name__icontains=query)
            )
        if accessory_finish:
            queryset = queryset.filter(finish__icontains=accessory_finish)
        if supplier:
            queryset = queryset.filter(supplier__name__icontains=supplier)
        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return ['masters/partials/accessory_list_partial.html']
        return ['masters/accessory_list.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['selected_finish'] = self.request.GET.get('finish', '')
        context['selected_supplier'] = self.request.GET.get('supplier', '')
        context['all_finishes'] = Accessory.objects.values_list('finish', flat=True).distinct().exclude(finish__isnull=True).exclude(finish__exact='')
        context['all_suppliers'] = Accessory.objects.values_list('supplier__name', flat=True).distinct().exclude(supplier__isnull=True).exclude(supplier__name__exact='')
        return context

class AccessoryCreateView(PermissionRequiredMixin, CreateView):
    model = Accessory
    template_name = 'masters/accessory_form.html'
    fields = ['name', 'code', 'description', 'finish', 'supplier', 'price', 'weight', 'unit', 'lead_time', 'stock', 'image']
    success_url = reverse_lazy('masters:accessory_list')
    permission_required = 'masters.add_accessory'

    def get_template_names(self):
        if self.request.htmx:
            return ['masters/partials/accessory_form_partial.html']
        return ['masters/accessory_form.html']

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx:
            messages.success(self.request, "Accessory created successfully!")
            self.object.refresh_from_db()
            return render(self.request, 'masters/partials/accessory_detail_partial.html', {'accessory': self.object})
        return response

class AccessoryDetailView(PermissionRequiredMixin, DetailView):
    model = Accessory
    template_name = 'masters/accessory_detail.html'
    context_object_name = 'accessory'
    permission_required = 'masters.view_accessory'

    def get_template_names(self):
        if self.request.htmx:
            return ['masters/partials/accessory_detail_partial.html']
        return ['masters/accessory_detail.html']

class AccessoryUpdateView(PermissionRequiredMixin, UpdateView):
    model = Accessory
    template_name = 'masters/accessory_form.html'
    fields = ['name', 'code', 'description', 'finish', 'supplier', 'price', 'weight', 'unit', 'lead_time', 'stock', 'image']
    success_url = reverse_lazy('masters:accessory_list')
    permission_required = 'masters.change_accessory'

    def get_template_names(self):
        if self.request.htmx:
            return ['masters/partials/accessory_form_partial.html']
        return ['masters/accessory_form.html']

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx:
            messages.success(self.request, "Accessory updated successfully!")
            self.object.refresh_from_db()
            return render(self.request, 'masters/partials/accessory_detail_partial.html', {'accessory': self.object})
        return response

class AccessoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = Accessory
    template_name = 'masters/accessory_confirm_delete.html'
    success_url = reverse_lazy('masters:accessory_list')
    permission_required = 'masters.delete_accessory'

    def get_template_names(self):
        if self.request.htmx:
            return ['masters/partials/accessory_confirm_delete_partial.html']
        return ['masters/accessory_confirm_delete.html']

    def form_valid(self, form):
        if self.request.htmx:
            self.object.delete()
            messages.success(self.request, "Accessory deleted successfully!")
            return HttpResponse(status=204, headers={'HX-Redirect': self.success_url})
        return super().form_valid(form)
