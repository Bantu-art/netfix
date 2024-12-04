from django.urls import path
from .views import (
    ServiceListView, ServiceCategoryListView, ServiceDetailView,
    ServiceCreateView, ServiceRequestCreateView, MostRequestedServicesView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', ServiceListView.as_view(), name='service-list'),
    path('category/<str:category>/', ServiceCategoryListView.as_view(), name='service-category'),
    path('create/', ServiceCreateView.as_view(), name='service-create'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('<int:pk>/request/', ServiceRequestCreateView.as_view(), name='service-request'),
    path('company/<int:pk>/', ServiceDetailView.as_view(), name='company-profile'),
    path('most-requested/', MostRequestedServicesView.as_view(), name='most-requested-services'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)