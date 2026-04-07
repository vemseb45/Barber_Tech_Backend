from django.db import models
from usuarios.models.usuario import Usuario
from barberias.models.barberia import Barberia
from barberias.models.especialidad import Especialidad


class BarberoDetalle(models.Model):

    cedula = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="cedula",
        related_name="detalle_barbero",
        limit_choices_to={"rol": "Barbero"}
    )

    barberia = models.ForeignKey(
        Barberia,
        on_delete=models.CASCADE,
        related_name="barberos"
    )

    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name="barberos"
    )

    class Meta:
        db_table = "barbero_detalle"

    def __str__(self):
        return f"{self.cedula.nombre} - {self.barberia.nombre}"