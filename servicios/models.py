from django.db import models

# Create your models here.
from django.db import models

class Servicio(models.Model):

    id_servicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_minutos = models.IntegerField()
    # Estos campos los tenías en tu modelo original de agenda
    id_barberia = models.IntegerField(default=1) 
    id_especialidad = models.IntegerField(default=1)

    class Meta:
        db_table = "servicio"

    def __str__(self):
        return self.nombre