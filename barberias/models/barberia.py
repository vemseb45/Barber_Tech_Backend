from django.db import models


class Barberia(models.Model):

    id_barberia = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=50)

    direccion = models.CharField(max_length=100)

    telefono = models.CharField(max_length=20)

    email = models.EmailField()

    class Meta:
        db_table = "barberia"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre