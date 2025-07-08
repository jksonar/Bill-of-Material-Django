from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Style, StyleFabricConsumption, StyleAccessoryConsumption

class StyleListView(ListView):
    model = Style
    template_name = 'styles/style_list.html'
    context_object_name = 'styles'

class StyleCreateView(CreateView):
    model = Style
    template_name = 'styles/style_form.html'
    fields = ['code', 'name', 'category', 'image']
    success_url = reverse_lazy('styles:style_list')

class StyleDetailView(DetailView):
    model = Style
    template_name = 'styles/style_detail.html'
    context_object_name = 'style'

class StyleUpdateView(UpdateView):
    model = Style
    template_name = 'styles/style_form.html'
    fields = ['code', 'name', 'category', 'image']
    success_url = reverse_lazy('styles:style_list')

class StyleDeleteView(DeleteView):
    model = Style
    template_name = 'styles/style_confirm_delete.html'
    success_url = reverse_lazy('styles:style_list')


class StyleFabricConsumptionCreateView(CreateView):
    model = StyleFabricConsumption
    template_name = 'styles/style_fabric_consumption_form.html'
    fields = ['fabric', 'quantity', 'unit']

    def form_valid(self, form):
        form.instance.style = Style.objects.get(pk=self.kwargs['style_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('styles:style_detail', kwargs={'pk': self.kwargs['style_pk']})

class StyleFabricConsumptionUpdateView(UpdateView):
    model = StyleFabricConsumption
    template_name = 'styles/style_fabric_consumption_form.html'
    fields = ['fabric', 'quantity', 'unit']

    def get_success_url(self):
        return reverse_lazy('styles:style_detail', kwargs={'pk': self.kwargs['style_pk']})

class StyleFabricConsumptionDeleteView(DeleteView):
    model = StyleFabricConsumption
    template_name = 'styles/style_fabric_consumption_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('styles:style_detail', kwargs={'pk': self.kwargs['style_pk']})


class StyleAccessoryConsumptionCreateView(CreateView):
    model = StyleAccessoryConsumption
    template_name = 'styles/style_accessory_consumption_form.html'
    fields = ['accessory', 'quantity', 'unit']

    def form_valid(self, form):
        form.instance.style = Style.objects.get(pk=self.kwargs['style_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('styles:style_detail', kwargs={'pk': self.kwargs['style_pk']})

class StyleAccessoryConsumptionUpdateView(UpdateView):
    model = StyleAccessoryConsumption
    template_name = 'styles/style_accessory_consumption_form.html'
    fields = ['accessory', 'quantity', 'unit']

    def get_success_url(self):
        return reverse_lazy('styles:style_detail', kwargs={'pk': self.kwargs['style_pk']})

class StyleAccessoryConsumptionDeleteView(DeleteView):
    model = StyleAccessoryConsumption
    template_name = 'styles/style_accessory_consumption_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('styles:style_detail', kwargs={'pk': self.kwargs['style_pk']})
