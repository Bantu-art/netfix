from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .forms import CustomerRegistrationForm, CompanyRegistrationForm
from .models import User

class CustomerRegistrationView(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'users/register_customer.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'customer'
        return context

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Registration successful! Please login.')
        return redirect(self.success_url)

class CompanyRegistrationView(CreateView):
    model = User
    form_class = CompanyRegistrationForm
    template_name = 'users/register_company.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'company'
        return context

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Registration successful! Please login.')
        return redirect(self.success_url)

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user