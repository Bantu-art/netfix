from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomerRegistrationView, CompanyRegistrationView, ProfileView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/customer/', CustomerRegistrationView.as_view(), name='register-customer'),
    path('register/company/', CompanyRegistrationView.as_view(), name='register-company'),
    path('profile/', ProfileView.as_view(), name='profile'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
