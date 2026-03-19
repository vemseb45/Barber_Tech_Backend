from django.db import models


class Especialidad(models.Model):

    id_especialidad = models.AutoField(primary_key=True)

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        db_table = "especialidad"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre