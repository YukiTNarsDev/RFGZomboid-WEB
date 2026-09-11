from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import EventNotice

def home_view(request):
    """
    Esta es la vista del 'Shell' o esqueleto de nuestra SPA.
    Siempre devuelve la página completa inicial.
    """
    # Si el usuario ya está logueado, lo mandamos al dashboard directamente
    if request.user.is_authenticated:
        return render(request, 'core/base.html', {'initial_partial': 'core/partials/dashboard.html'})
    
    # Si no, cargamos la base con el formulario de login incrustado
    return render(request, 'core/base.html', {'initial_partial': 'core/partials/login_form.html'})

def get_login_form(request):
    """Devuelve únicamente el HTML del formulario para inyectarlo en el header."""
    form = AuthenticationForm()
    return render(request, 'core/partials/login_form.html', {'form': form})

@login_required # Protegemos la vista: solo usuarios logueados pueden entrar
def dashboard_view(request):
    """
    Fragmento HTML del panel de control principal.
    """
    return render(request, 'core/partials/dashboard.html')



def events_list_view(request):
    # Obtenemos los eventos ordenados por los más recientes
    event_list = EventNotice.objects.all().order_by('-created_at')
    
    # Dividimos los resultados en bloques de 10
    paginator = Paginator(event_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/partials/event_items.html', {'page_obj': page_obj})