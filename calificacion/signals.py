from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime

from cita.models import Cita
from .models import Calificacion  # ajusta si es necesario


@receiver(post_save, sender=Cita)
def crear_calificacion_cuando_finaliza(sender, instance, created, **kwargs):
    
    # Combinar fecha + hora
    fecha_hora_cita = datetime.combine(instance.fecha, instance.hora)

    # Convertir a timezone-aware
    fecha_hora_cita = timezone.make_aware(fecha_hora_cita)

    ahora = timezone.now()

    # Validar si ya pasó la cita
    if fecha_hora_cita < ahora and not hasattr(instance, 'calificacion'):
        Calificacion.objects.create(
            cita=instance,
            barbero=instance.cedula_barbero,
            cliente=instance.cedula_cliente
        )