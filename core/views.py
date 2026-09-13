from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import EventNotice

def dashboard_view(request):
    """
    Punto de entrada principal. 
    Siempre devuelve la estructura del dashboard. Las secciones privadas 
    se ocultarán o mostrarán dentro del template usando {% if request.user.is_authenticated %}
    """
    return render(request, '\core\dashboard.html')

def login_view(request):
    """
    Esta vista maneja exclusivamente el popup de login mediante HTMX.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) # Inicia sesión en el backend
            
            # ¿Por qué usamos HX-Refresh?
            # Al autenticarse con éxito, necesitamos que todo el dashboard se reconstruya
            # para que Django evalúe los permisos (ej. request.user.role == 'PAGO') de forma segura en el servidor.
            # HX-Refresh le indica al navegador que haga una recarga limpia.
            response = HttpResponse()
            response['HX-Refresh'] = "true"
            return response
        else:
            # Si hay error (contraseña incorrecta), devolvemos el formulario con los errores
            # para que HTMX lo reemplace dentro del popup sin cerrar el modal.
            return render(request, 'core/partials/modal_login.html', {'form': form})

    # Si la petición es GET (cuando el usuario hace clic en el botón de login),
    # devolvemos el HTML del formulario vacío.
    form = AuthenticationForm()
    return render(request, 'core/partials/modal_login.html', {'form': form})