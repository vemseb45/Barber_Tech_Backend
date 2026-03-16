from datetime import datetime, timedelta
from .models import AgendaBarbero, Cita

def calcular_disponibilidad(cedula_barbero, fecha_str):
    # 1. Saber qué día de la semana es (Lunes, Martes...)
    dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    dia_nombre = dias_semana[fecha_obj.weekday()]

    # 2. Consultar el horario del barbero ese día
    try:
        horario = AgendaBarbero.objects.get(cedula_barbero=cedula_barbero, dia=dia_nombre)
    except AgendaBarbero.DoesNotExist:
        return [] # El barbero no trabaja ese día

    # 3. Buscar las citas que ya están ocupadas ese día
    citas_ocupadas = Cita.objects.filter(
        cedula_barbero=cedula_barbero, 
        fecha=fecha_obj
    ).values_list('hora', flat=True)

    # 4. Generar los bloques de tiempo (Ej: cada 1 hora)
    bloques = []
    hora_actual = datetime.combine(fecha_obj, horario.hora_inicio)
    hora_fin = datetime.combine(fecha_obj, horario.hora_fin)

    while hora_actual < hora_fin:
        estado = "ocupado" if hora_actual.time() in citas_ocupadas else "disponible"
        
        bloques.append({
            "hora": hora_actual.strftime('%I:%M %p'), # Lo que ve el usuario (09:00 AM)
            "hora_db": hora_actual.strftime('%H:%M:%S'), # Lo que enviamos al POST (09:00:00)
            "estado": estado
        })
        hora_actual += timedelta(hours=1) # Intervalo de 1 hora

    return bloques