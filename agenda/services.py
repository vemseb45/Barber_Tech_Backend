from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError

from .models import AgendaBarbero
from cita.models import Cita
from servicios.services.servicio_service import ServicioService


# ======================================================
# DISPONIBILIDAD (NO CAMBIA FUNCIONALIDAD)
# ======================================================

def calcular_disponibilidad(cedula_barbero, fecha_str):

    dias_semana = [
        'Lunes', 'Martes', 'Miercoles',
        'Jueves', 'Viernes', 'Sabado', 'Domingo'
    ]

    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    dia_nombre = dias_semana[fecha_obj.weekday()]

    try:
        horario = AgendaBarbero.objects.get(
            cedula_barbero=cedula_barbero,
            dia=dia_nombre
        )
    except AgendaBarbero.DoesNotExist:
        return []

    citas_ocupadas = Cita.objects.filter(
        cedula_barbero_id=cedula_barbero,
        fecha=fecha_obj
    ).values_list('hora', flat=True)

    bloques = []
    hora_actual = datetime.combine(fecha_obj, horario.hora_inicio)
    hora_fin = datetime.combine(fecha_obj, horario.hora_fin)

    while hora_actual < hora_fin:

        estado = "ocupado" if hora_actual.time() in citas_ocupadas else "disponible"

        bloques.append({
            "hora": hora_actual.strftime('%I:%M %p'),
            "hora_db": hora_actual.strftime('%H:%M:%S'),
            "estado": estado
        })

        hora_actual += timedelta(hours=1)

    return bloques


# ======================================================
# NUEVO — RESERVAR CITA INTEGRADO CON SERVICIOS
# ======================================================

def reservar_cita(
    barbero_cedula,
    cliente_cedula,
    fecha,
    hora_inicio,
    duracion_servicio=None,
    id_servicio=None
):

    if not id_servicio:
        raise ValidationError("El servicio es obligatorio")

    # ✅ duración oficial del servicio
    duracion_real = ServicioService.obtener_duracion(id_servicio)

    # ✅ compatibilidad con frontend actual
    if duracion_servicio:

        if int(duracion_servicio) != int(duracion_real):
            raise ValidationError(
                "La duración enviada no coincide con el servicio."
            )

    duracion = duracion_real

    hora_fin = (
        datetime.combine(fecha, hora_inicio)
        + timedelta(minutes=duracion)
    ).time()

    # ====================================
    # VALIDAR HORARIO BARBERO
    # ====================================

    dias_semana = [
        'Lunes', 'Martes', 'Miercoles',
        'Jueves', 'Viernes', 'Sabado', 'Domingo'
    ]

    dia_nombre = dias_semana[fecha.weekday()]

    agenda = AgendaBarbero.objects.filter(
        cedula_barbero=barbero_cedula,
        dia__iexact=dia_nombre
    ).first()

    if not agenda:
        raise ValidationError("El barbero no trabaja ese día.")

    if not (agenda.hora_inicio <= hora_inicio < agenda.hora_fin):
        raise ValidationError("Fuera del horario laboral.")

    # ====================================
    # VALIDAR CRUCE DE CITAS
    # ====================================

    citas = Cita.objects.filter(
        cedula_barbero_id=barbero_cedula,
        fecha=fecha
    )

    for cita in citas:

        duracion_existente = ServicioService.obtener_duracion(
            cita.servicio_id
        )

        fin_existente = (
            datetime.combine(fecha, cita.hora)
            + timedelta(minutes=duracion_existente)
        ).time()

        if (hora_inicio < fin_existente and hora_fin > cita.hora):
            raise ValidationError(
                "El horario ya está ocupado."
            )

    # ====================================
    # CREAR CITA
    # ====================================

    nueva_cita = Cita.objects.create(
        fecha=fecha,
        hora=hora_inicio,
        servicio_id=id_servicio,
        cedula_cliente_id=cliente_cedula,
        cedula_barbero_id=barbero_cedula
    )

    return nueva_cita