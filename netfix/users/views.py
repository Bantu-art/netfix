from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .forms import CustomerRegistrationForm, CompanyRegistrationForm
from .models import User
from django.contrib.auth import login


class CustomerRegistrationView(CreateView):
    """
    Handle customer user registration.
    
    Attributes:
        model: User model
        form_class: Form for customer registration
        template_name: Path to template
        success_url: Redirect URL after successful registration
    """
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'users/register_customer.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        """
        Add user type to context.
        
        Returns:
            dict: Context with user_type='customer'
        """
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'customer'
        return context

    def form_valid(self, form):
        """
        Process valid form data and login user.
        
        Args:
            form: Valid registration form
            
        Returns:
            HttpResponse: Redirect to success URL
            
        Notes:
            - Sets is_company to False
            - Automatically logs in the user
            - Displays success message
        """
        user = form.save()
        user.is_company = False
        user.save()
        
        login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return redirect(self.success_url)


class CompanyRegistrationView(CreateView):
    """
    Handle service provider company registration.
    
    Attributes:
        model: User model
        form_class: Form for company registration
        template_name: Path to template
        success_url: Redirect URL after successful registration
    """
    model = User
    form_class = CompanyRegistrationForm
    template_name = 'users/register_company.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        """
        Add user type to context.
        
        Returns:
            dict: Context with user_type='company'
        """
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'company'
        return context

    def form_valid(self, form):
        """
        Process valid form data and login user.
        
        Args:
            form: Valid registration form
            
        Returns:
            HttpResponse: Redirect to success URL
            
        Notes:
            - Sets is_company to True
            - Automatically logs in the user
            - Displays success message
        """
        user = form.save()
        user.is_company = True
        user.save()
        
        login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return redirect(self.success_url)


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Display user profile information.
    
    Attributes:
        model: User model
        template_name: Path to template
        context_object_name: Name used in template context
        
    Notes:
        Requires user authentication (LoginRequiredMixin)
    """
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        """
        Return the currently logged-in user.
        
        Returns:
            User: Current authenticated user instance
        """
        return self.request.user