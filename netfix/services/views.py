from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Service, ServiceRequest
from .forms import ServiceForm, ServiceRequestForm
from django.db.models import Count
from django.views.generic import ListView

class MostRequestedServicesView(ListView):
    model = Service
    template_name = 'services/most_requested_services.html'
    context_object_name = 'most_requested_services'

    def get_queryset(self):
        # Count the number of requests for each service and order by request count
        return Service.objects.annotate(
            request_count=Count('requests')
        ).order_by('-request_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add total request count for each service
        for service in context['most_requested_services']:
            service.total_requests = service.requests.count()
        return context

class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Service.objects.all()
        field = self.kwargs.get('field')
        if field:
            queryset = queryset.filter(field=field)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_fields'] = Service.FIELD_CHOICES
        return context

class ServiceCategoryListView(ListView):
    model = Service
    template_name = 'services/service_category_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(field=self.kwargs['category']).order_by('-created_at')

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_create.html'
    success_url = reverse_lazy('service-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.company = self.request.user
        messages.success(self.request, 'Service created successfully!')
        return super().form_valid(form)

class ServiceRequestCreateView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'services/service_request.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(Service, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.customer = self.request.user
        form.instance.service = get_object_or_404(Service, pk=self.kwargs['pk'])
        messages.success(self.request, 'Service requested successfully!')
        return super().form_valid(form)