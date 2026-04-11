# agenda/utils/agenda.py
from datetime import datetime, timedelta
from cita.models import Cita
from ..models import AgendaBarbero
from usuarios.models.usuario import Usuario

def obtener_cedula_barbero(barbero_id):
    try:
        usuario = Usuario.objects.get(id=barbero_id)
        return usuario.cedula
    except Usuario.DoesNotExist:
        return None

def obtener_disponibilidad_opt(cedula_barbero, fecha, duracion):
    """
    Devuelve bloques de horario disponibles para un barbero
    """
    # Tu lógica aquí
    bloques = []
    # ejemplo dummy
    bloques.append((datetime.strptime("09:00", "%H:%M").time(),
                    datetime.strptime("10:00", "%H:%M").time()))
    return bloques