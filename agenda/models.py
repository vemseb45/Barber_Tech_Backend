# models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta, datetime, time

class Usuario(models.Model):
    cedula = models.CharField(primary_key=True, max_length=11)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    # rol y estado usarían enums de tu DB
    rol = models.CharField(max_length=10)
    estado = models.CharField(max_length=10)

class AgendaBarbero(models.Model):
    cedula_barbero = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cedula_barbero')
    dia = models.CharField(max_length=10)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

class Cita(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cedula_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='citas_cliente')
    cedula_barbero = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='citas_barbero')
    id_servicio = models.IntegerField()