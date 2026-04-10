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
        max_length=10, 
        choices=ROLES, 
        default='Cliente'
    )
    
    cedula = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=10)
    estado = models.CharField(max_length=10, default='Activo') 

    def __str__(self):
        return f"{self.cedula} - {self.username} - {self.rol}"