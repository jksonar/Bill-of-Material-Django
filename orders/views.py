from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, CreateView
from django.urls import reverse_lazy
from .models import Order, BOMFabric, BOMAccessory, BOMVersion
from styles.models import Style
from django.db.models import Q

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        customer = self.request.GET.get('customer')
        style = self.request.GET.get('style')
        search_query = self.request.GET.get('q')

        if status:
            queryset = queryset.filter(status=status)
        if customer:
            queryset = queryset.filter(customer__icontains=customer)
        if style:
            queryset = queryset.filter(style__name__icontains=style)
        if search_query:
            queryset = queryset.filter(
                Q(order_no__icontains=search_query) |
                Q(customer__icontains=search_query) |
                Q(style__name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_statuses'] = Order.STATUS_CHOICES
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_customer'] = self.request.GET.get('customer', '')
        context['selected_style'] = self.request.GET.get('style', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = ['order_no', 'customer', 'style', 'quantity', 'due_date', 'status']
    success_url = reverse_lazy('orders:order_list')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object

        # Get all BOM versions for this order
        all_bom_versions = BOMVersion.objects.filter(order=order).order_by('-version_number')
        context['all_bom_versions'] = all_bom_versions

        # Determine which BOM version to display
        selected_version_id = self.request.GET.get('version')
        if selected_version_id:
            selected_version = all_bom_versions.filter(pk=selected_version_id).first()
        else:
            selected_version = all_bom_versions.first() # Default to latest

        context['selected_bom_version'] = selected_version

        if selected_version:
            context['bom_fabrics'] = BOMFabric.objects.filter(order=order, version=selected_version)
            context['bom_accessories'] = BOMAccessory.objects.filter(order=order, version=selected_version)
        else:
            context['bom_fabrics'] = BOMFabric.objects.none()
            context['bom_accessories'] = BOMAccessory.objects.none()

        # Get style costing information
        style_costing = order.style.stylecosting
        if style_costing:
            context['total_order_cost'] = style_costing.total_cost * order.quantity
            context['total_order_landed_cost'] = style_costing.landed_cost * order.quantity
            context['total_order_retail_price'] = style_costing.retail_price * order.quantity
        else:
            context['total_order_cost'] = 0
            context['total_order_landed_cost'] = 0
            context['total_order_retail_price'] = 0

        return context

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = ['order_no', 'customer', 'style', 'quantity', 'due_date', 'status']
    success_url = reverse_lazy('orders:order_list')

class BOMFabricUpdateView(LoginRequiredMixin, UpdateView):
    model = BOMFabric
    template_name = 'orders/bom_fabric_form.html'
    fields = ['issued_qty', 'balance']

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.order.pk})

class BOMAccessoryUpdateView(LoginRequiredMixin, UpdateView):
    model = BOMAccessory
    template_name = 'orders/bom_accessory_form.html'
    fields = ['issued_qty', 'balance']

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.order.pk})

class BOMSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/bom_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_bom_fabrics'] = BOMFabric.objects.all()
        context['all_bom_accessories'] = BOMAccessory.objects.all()
        return context
