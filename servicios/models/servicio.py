from django.db import models
from barberias.models import Barberia, Especialidad

class Servicio(models.Model):

    id_servicio = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=100)

    descripcion = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duracion_minutos = models.IntegerField()

    #importa tabla barberia
    barberia = models.ForeignKey(
    Barberia,
    on_delete=models.CASCADE,
    related_name="servicios"
    )

    #importa tabla especialidad y obtiene ID especialidad
    especialidad = models.ForeignKey(
    Especialidad,
    on_delete=models.PROTECT,
    related_name="servicios"
    )

    class Meta:
        db_table = "servicio"

    def __str__(self):
        return f"{self.nombre} ({self.duracion_minutos} min)"