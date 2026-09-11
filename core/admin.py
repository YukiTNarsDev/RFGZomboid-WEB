from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Ticket, EventNotice

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Heredamos de UserAdmin porque Django ya tiene una interfaz muy compleja y segura 
    para manejar contraseñas encriptadas y permisos. Si heredamos de ModelAdmin normal, 
    romperíamos el formulario de cambiar contraseña.
    """
    # Añadimos nuestro campo 'role' a la interfaz de edición, creando una nueva sección visual.
    fieldsets = UserAdmin.fieldsets + (
        ('Roles y Permisos de Zomboid', {'fields': ('role',)}),
    )
    
    # list_display: ¿Qué columnas queremos ver en la tabla general?
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    
    # list_filter: Crea un panel lateral para filtrar rápidamente (ej. "Mostrar solo usuarios PAGO")
    list_filter = ('role', 'is_staff', 'is_active')
    
    # search_fields: Crea una barra de búsqueda en la parte superior.
    search_fields = ('username', 'email')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Aquí aplicamos principios de Observabilidad: Queremos ver de un vistazo 
    qué tickets están abiertos, quién los creó y cuándo.
    """
    list_display = ('title', 'author', 'ticket_type', 'status', 'created_at')
    list_filter = ('status', 'ticket_type', 'created_at')
    
    # Nota de Senior: Para buscar por campos de una relación (Foreign Key), 
    # usamos la sintaxis modelo__campo (author__username)
    search_fields = ('title', 'description', 'author__username')
    
    # Protegemos los campos de auditoría para que nadie pueda editarlos manualmente.
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EventNotice)
class EventNoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'component', 'impact', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description', 'event_type', 'component', 'impact')