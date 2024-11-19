from django.views.generic import TemplateView
from services.models import Service, ServiceRequest
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout





class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_services'] = Service.objects.annotate(
            request_count=Count('requests')
        ).order_by('-request_count')[:5]
        return context
    

@login_required
def logout_view(request):
    if request.method == 'POST':
        username = request.user.username  # Get username before logout
        logout(request)
        messages.success(request, f'Bye {username}, hope to see you soon!')
        return redirect('home')  # or whatever your home URL name is
    return redirect('profile')  # redirect to profile if someone tries to GET this URL
