from django.db import models
from servicios.models import Servicio  # <--- Ahora esto ya no fallará

from usuarios.models import Usuario

class Cita(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    cedula_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='citas_cliente')
    cedula_barbero = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='citas_barbero')

    class Meta:
        db_table = 'agenda_cita'