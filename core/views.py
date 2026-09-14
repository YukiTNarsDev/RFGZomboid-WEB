from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import EventNotice

def home_view(request):
    """
    Punto de entrada principal. 
    Siempre devuelve la estructura del dashboard. Las secciones privadas 
    se evalúan directamente dentro del HTML usando {% if request.user.is_authenticated %}
    """
    return render(request, 'core/partials/dashboard.html')


def login_view(request):
    """
    Maneja exclusivamente el popup de login mediante HTMX.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) # Inicia sesión segura en el backend
            
            # Al loguearnos, obligamos al navegador a recargar el dashboard 
            # para que Django renderice los paneles VIP o tickets si corresponde.
            response = HttpResponse()
            response['HX-Refresh'] = "true"
            return response
        else:
            # Si la contraseña es incorrecta, devolvemos el formulario con los errores
            # HTMX lo inyectará dentro del mismo popup sin cerrarlo.
            return render(request, 'core/partials/modal_login.html', {'form': form})

    # Petición GET: Devuelve el formulario vacío cuando se hace clic en "Iniciar Sesión"
    form = AuthenticationForm()
    return render(request, 'core/partials/modal_login.html', {'form': form})


def logout_view(request):
    """
    Destruye la sesión del usuario y refresca la interfaz.
    """
    if request.method == 'POST':
        logout(request)
        response = HttpResponse()
        response['HX-Refresh'] = "true"
        return response
    
    return HttpResponse(status=405)