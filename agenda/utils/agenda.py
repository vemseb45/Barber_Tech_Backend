# agenda/utils/agenda.py
from datetime import datetime, timedelta
from ..models import Cita, AgendaBarbero

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