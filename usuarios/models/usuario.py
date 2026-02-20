from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):

    ROLES = [
        ('Cliente', 'Cliente'),
        ('Barbero', 'Barbero'),
        ('Admin', 'Admin'),
    ]

    ESTADOS = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    cedula = models.CharField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20, unique=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='Cliente')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Activo')

    REQUIRED_FIELDS = ['email', 'cedula', 'telefono']

    def __str__(self):
        return self.username