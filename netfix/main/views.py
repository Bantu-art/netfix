from django.views.generic import TemplateView
from services.models import Service, ServiceRequest
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout


class HomeView(TemplateView):
    """
    View for rendering the home page of the application.
    Displays the 5 most popular services based on request count.
    
    Inherits from:
        TemplateView: Django's generic template view
    """
    
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        """
        Extends the context data with popular services.
        
        Args:
            **kwargs: Additional keyword arguments passed to the view
            
        Returns:
            dict: Context dictionary containing popular services
        """
        context = super().get_context_data(**kwargs)
        context['popular_services'] = Service.objects.annotate(
            request_count=Count('requests')
        ).order_by('-request_count')[:5]
        return context


@login_required
def logout_view(request):
    """
    Handles user logout functionality.
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponseRedirect: Redirects to 'home' page after successful POST logout
        or to 'profile' page for GET requests
        
    Notes:
        - Requires user to be logged in (login_required decorator)
        - Only processes logout on POST requests
        - Displays a farewell message using Django's message framework
    """
    if request.method == 'POST':
        username = request.user.username 
        logout(request)
        messages.success(request, f'Bye {username}, hope to see you soon!')
        return redirect('home') 
    return redirect('profile')  # redirect to profile if someone tries to GET this URL
