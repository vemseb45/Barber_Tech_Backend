from django.db import models
from servicios.models import Servicio
from usuarios.models import Usuario

class Cita(models.Model):
    ESTADOS = [
        ('PENT', 'Pendiente'),
        ('CONF', 'Confirmada'),
        ('CANC', 'Cancelada'),
    ]
    
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS, 
        default='PENT',
    )

    fecha = models.DateField()
    hora = models.TimeField()

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    cedula_cliente = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='citas_cliente'
    )
    cedula_barbero = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='citas_barbero'
    )

    class Meta:
        db_table = 'agenda_cita'

    # ✅ AQUÍ ADENTRO (bien indentado)
    def __str__(self):
        return f"Cita #{self.id} - {self.fecha} {self.hora} - {self.cedula_barbero}"