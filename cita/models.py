from django.db import models
from servicios.models import Servicio  # <--- Ahora esto ya no fallará

class Cita(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    # Usamos la relación real
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, db_column='id_servicio')
    
    cedula_cliente_id = models.CharField(max_length=50)
    cedula_barbero_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'agenda_cita'