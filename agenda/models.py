# agenda/models.py
from django.db import models

class Usuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    # 🚨 AGREGA ESTA LÍNEA (Es la que falta)
    rol = models.CharField(max_length=50) 

    class Meta:
        db_table = 'usuarios_usuario'
        managed = False
# agenda/models.py

class AgendaBarbero(models.Model):
    # Lo cambiamos a CharField porque en la DB es texto (Varchar)
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
    # En tu imagen 0f507f.png las columnas son 'cedula_barbero_id' y 'cedula_cliente_id'
    cedula_cliente = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        db_column='cedula_cliente_id', 
        related_name='citas_cliente'
    )
    cedula_barbero = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        db_column='cedula_barbero_id', 
        related_name='citas_barbero'
    )
    id_servicio = models.IntegerField()

    class Meta:
        db_table = 'agenda_cita'
        managed = False


class Cita(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    id_servicio = models.IntegerField()
    # Usamos CharField para evitar el choque de tipos con PostgreSQL
    cedula_cliente_id = models.CharField(max_length=50)
    cedula_barbero_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'agenda_cita'
        managed = False