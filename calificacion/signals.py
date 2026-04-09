from django.db.models.signals import post_save
from django.dispatch import receiver
from cita.models import Cita
from .models import Calificacion
from datetime import datetime

@receiver(post_save, sender=Cita)
def crear_calificacion_cuando_finaliza(sender, instance, created, **kwargs):
    """
    Se ejecuta cada vez que se guarda una cita
    """
    ahora = datetime.now()

    # Si la cita ya pasó y no tiene calificación
    if instance.fecha < ahora and not hasattr(instance, 'calificacion'):
        # Solo crea un placeholder (sin puntuación aún)
        Calificacion.objects.create(cita=instance)