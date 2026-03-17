from django.db import models


class Usuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    rol = models.CharField(max_length=50)

    class Meta:
        db_table = 'usuarios_usuario'
        managed = False


class AgendaBarbero(models.Model):
    cedula_barbero = models.CharField(max_length=50, db_column='cedula_barbero')
    dia = models.CharField(max_length=10)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        db_table = 'agenda_agendabarbero'
        managed = False


class Cita(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    id_servicio = models.IntegerField()

    # Usamos CharField para evitar conflicto de tipos con PostgreSQL
    cedula_cliente_id = models.CharField(max_length=50)
    cedula_barbero_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'agenda_cita'
        managed = False