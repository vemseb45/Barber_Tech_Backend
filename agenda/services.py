# agenda/services.py
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from .models import Cita
from .utils.agenda import obtener_disponibilidad_opt

def reservar_cita(cedula_barbero, cedula_cliente, fecha_str, hora_str, duracion, id_servicio):
    """
    Lógica de reserva de cita centralizada
    """
    # Convertir fecha y hora
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora_inicio = datetime.strptime(hora_str, '%H:%M:%S').time()
    except ValueError:
        raise ValidationError("Formato de fecha u hora inválido")

    # Calcular bloques disponibles
    bloques_disponibles = obtener_disponibilidad_opt(cedula_barbero, fecha, duracion)
    hora_fin = (datetime.combine(fecha, hora_inicio) + timedelta(minutes=duracion)).time()

    # Validación de disponibilidad
    if (hora_inicio, hora_fin) not in bloques_disponibles:
        raise ValidationError("Horario no disponible")

    # Crear cita
    cita = Cita.objects.create(
        fecha=fecha,
        hora=hora_inicio,
        cedula_cliente_id=cedula_cliente,
        cedula_barbero_id=cedula_barbero,
        id_servicio=id_servicio
    )
    return cita