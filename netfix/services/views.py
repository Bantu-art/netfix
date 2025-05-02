from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Service, ServiceRequest
from .forms import ServiceForm, ServiceRequestForm
from django.db.models import Count


class MostRequestedServicesView(LoginRequiredMixin, ListView):
    """
    Display services ordered by number of requests.
    
    Attributes:
        model: Service model
        template_name: Path to template
        context_object_name: Name used in template context
    
    Notes:
        Requires user authentication
    """
    model = Service
    template_name = 'services/most_requested_services.html'
    context_object_name = 'most_requested_services'
    
    def get_queryset(self):
        """
        Retrieve services with requests, ordered by request count.
        
        Returns:
            QuerySet: Filtered and annotated Service objects
        """
        return Service.objects.filter(requests__isnull=False).annotate(
            request_count=Count('requests')
        ).order_by('-request_count')

    def get_context_data(self, **kwargs):
        """
        Add total request count for each service to context.
        
        Returns:
            dict: Context with enhanced service information
        """
        context = super().get_context_data(**kwargs)
        for service in context['most_requested_services']:
            service.total_requests = service.requests.count()
        return context


class ServiceListView(ListView):
    """
    Display list of all services with optional field filtering.
    
    Attributes:
        model: Service model
        template_name: Path to template
        context_object_name: Name used in template context
        ordering: Default ordering for queryset
    """
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Filter services by field if specified in URL kwargs.
        
        Returns:
            QuerySet: Filtered Service objects
        """
        queryset = Service.objects.all()
        field = self.kwargs.get('field')
        if field:
            queryset = queryset.filter(field=field)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Add service field choices to context.
        
        Returns:
            dict: Context with service fields
        """
        context = super().get_context_data(**kwargs)
        context['service_fields'] = Service.FIELD_CHOICES
        return context


class ServiceCategoryListView(ListView):
    """
    Display services filtered by category.
    
    Attributes:
        model: Service model
        template_name: Path to template
        context_object_name: Name used in template context
    """
    model = Service
    template_name = 'services/service_category_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        """
        Filter services by category from URL kwargs.
        
        Returns:
            QuerySet: Category-filtered Service objects
        """
        return Service.objects.filter(field=self.kwargs['category']).order_by('-created_at')


class ServiceDetailView(DetailView):
    """
    Display detailed information about a specific service.
    
    Attributes:
        model: Service model
        template_name: Path to template
        context_object_name: Name used in template context
    """
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'


class ServiceCreateView(LoginRequiredMixin, CreateView):
    """
    Handle creation of new services.
    
    Attributes:
        model: Service model
        form_class: Form for service creation
        template_name: Path to template
        success_url: Redirect URL after successful creation
        
    Notes:
        Requires user authentication
    """
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_create.html'
    success_url = reverse_lazy('service-list')

    def get_form_kwargs(self):
        """
        Add user to form kwargs for validation.
        
        Returns:
            dict: Updated form kwargs
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Set service company and display success message.
        
        Args:
            form: Valid service form
            
        Returns:
            HttpResponse: Redirect to success URL
        """
        form.instance.company = self.request.user
        messages.success(self.request, 'Service created successfully!')
        return super().form_valid(form)


class ServiceRequestCreateView(LoginRequiredMixin, CreateView):
    """
    Handle creation of service requests.
    
    Attributes:
        model: ServiceRequest model
        form_class: Form for request creation
        template_name: Path to template
        success_url: Redirect URL after successful creation
        
    Notes:
        Requires user authentication
    """
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'services/service_request.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        """
        Add requested service to context.
        
        Returns:
            dict: Context with service information
        """
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(Service, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Set request customer and service, display success message.
        
        Args:
            form: Valid request form
            
        Returns:
            HttpResponse: Redirect to success URL
        """
        form.instance.customer = self.request.user
        form.instance.service = get_object_or_404(Service, pk=self.kwargs['pk'])
        messages.success(self.request, 'Service requested successfully!')
        return super().form_valid(form)