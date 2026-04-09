from django.db import models
from cita.models import Cita

class Calificacion(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    cita = models.OneToOneField(
        Cita,
        on_delete=models.CASCADE,
        related_name='calificacion'
    )
    puntuacion = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calificación {self.puntuacion} - Cita {self.cita.id_cita}"