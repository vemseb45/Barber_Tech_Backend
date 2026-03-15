from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

    # Definimos las opciones del rol
    ROLES = [
        ('Cliente', 'Cliente'),
        ('Barbero', 'Barbero'),
        ('Admin', 'Administrador'),
    ]
    
    rol = models.CharField(
        max_length=20, 
        choices=ROLES, 
        default='Cliente'
    )
    
    cedula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=20, default='Activo')

    def __str__(self):
        return f"{self.username} - {self.rol}"