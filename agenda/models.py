from django.db import models

class AgendaBarbero(models.Model):
    cedula_barbero = models.CharField(max_length=50, db_column='cedula_barbero')
    dia = models.CharField(max_length=10) # Lunes, Martes, etc.
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        db_table = 'agenda_agendabarbero'