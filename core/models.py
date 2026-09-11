from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('gm', 'Game Master'),
        ('paid', 'Paid User'),
        ('free', 'Free User')
    )
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='free' # Por seguridad, todo nuevo registro es FREE por defecto
    )
    def __str__(self):
        # Esta función define cómo se representa el objeto en texto (útil para el panel de admin)
        return f"{self.username} ({self.get_role_display()})"

class Ticket(models.Model):
    TYPE_CHOICES = (
        ('bug', 'Bug/Error'),
        ('problem', 'Problema Técnico'),
        ('mod', 'Recomendación de Mod'),
    )

    STATUS_CHOICES = (
        ('open', 'Abierto'),
        ('in_progress', 'En Progreso'),
        ('closed', 'Cerrado'),
    )
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    ticket_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='PROBLEM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )

    created_at = models.DateTimeField(auto_now_add=True) # Se llena solo al CREAR el registro
    updated_at = models.DateTimeField(auto_now=True)     # Se actualiza solo CADA VEZ que se guarda

    def __str__(self):
        return f"[{self.status}] {self.title} - {self.author.username}"

class EventNotice(models.Model):
    EVENT_TYPE_CHOICES = (
        ('maintenance', 'Mantenimiento'),
        ('update', 'Actualización'),
        ('downtime', 'Caída del Servicio'),
        ('other', 'Otro'),
        ('evento', 'Evento Especial')
    )
    COMPONENT_CHOICES = (
        ('server', 'Servidor'),
        ('website', 'Sitio Web'),
        ('database', 'Base de Datos'),
        ('other', 'Otro'),
        ('bot', 'Bot de Discord')
    )
    IMPACT_CHOICES = (
        ('no_impact', 'Sin Impacto'),
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta')
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    component = models.CharField(max_length=20, choices=COMPONENT_CHOICES, default='other')
    impact = models.CharField(max_length=20, choices=IMPACT_CHOICES, default='no_impact', blank=True, null=True)
    start_time = models.DateTimeField(help_text="Fecha y hora de inicio del mantenimiento")
    end_time = models.DateTimeField(help_text="Fecha y hora estimada de finalización")
    is_active = models.BooleanField(default=True)


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mantenimiento: {self.title} ({'Activo' if self.is_active else 'Inactivo'})"