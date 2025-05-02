"""
URL configuration for the services application.

This module defines the URL patterns for all service-related views including:
- Service listing and filtering
- Service creation and detail views
- Service request handling
- Company profiles
- Most requested services

The urlpatterns list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.urls import path
from .views import (
    ServiceListView, ServiceCategoryListView, ServiceDetailView,
    ServiceCreateView, ServiceRequestCreateView, MostRequestedServicesView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Main service listing
    path('', ServiceListView.as_view(), name='service-list'),
    
    # Category-filtered service listing
    path('category/<str:category>/', ServiceCategoryListView.as_view(), name='service-category'),
    
    # Service creation
    path('create/', ServiceCreateView.as_view(), name='service-create'),
    
    # Individual service detail
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    
    # Service request creation
    path('<int:pk>/request/', ServiceRequestCreateView.as_view(), name='service-request'),
    
    # Company profile view
    path('company/<int:pk>/', ServiceDetailView.as_view(), name='company-profile'),
    
    # Most requested services listing
    path('most-requested/', MostRequestedServicesView.as_view(), name='most-requested-services'),
] 

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)