from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BarberoSerializer, CitaSerializer
from .models import Usuario, AgendaBarbero, Cita
from datetime import datetime, timedelta

# 1. LISTA DE BARBEROS
class ListaBarberosView(APIView):
    def get(self, request):
        barberos = Usuario.objects.filter(rol__iexact='Barbero')
        print(f"DEBUG: Se encontraron {barberos.count()} barberos en la base de datos.")
        
        serializer = BarberoSerializer(barberos, many=True)
        data = [{
            "id": str(b['id']),
            "nombre": b['username'],
            "especialidad": "Barbero Profesional"
        } for b in serializer.data]
        
        return Response(data)

# 2. DISPONIBILIDAD
class DisponibilidadBarbero(APIView):
    def get(self, request):
        barbero_id = request.query_params.get('barberoId')
        fecha_str = request.query_params.get('fecha')

        if not barbero_id or not fecha_str:
            return Response([], status=200)

        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
            dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
            nombre_dia = dias_semana[fecha_obj.weekday()]

            horario_base = AgendaBarbero.objects.filter(
                cedula_barbero=str(barbero_id), 
                dia=nombre_dia
            ).first()

            if not horario_base:
                return Response([], status=200)

            horas_disponibles = []
            actual = datetime.combine(fecha_obj, horario_base.hora_inicio)
            fin = datetime.combine(fecha_obj, horario_base.hora_fin)

            # --- EL ARREGLO ESTÁ AQUÍ ---
            while actual < fin:
                # En lugar de solo texto, enviamos el OBJETO que React espera
                horas_disponibles.append({
                    "hora": actual.strftime('%H:%M'),       # Lo que se ve en el botón
                    "hora_db": actual.strftime('%H:%M:%S')  # Lo que se guarda en la DB
                })
                actual += timedelta(minutes=60)

            # Consultamos citas existentes
            citas_existentes = Cita.objects.filter(
                cedula_barbero_id=str(barbero_id),
                fecha=fecha_str
            ).values_list('hora', flat=True)
            
            # Formateamos citas para comparar
            citas_formateadas = [c.strftime('%H:%M') for c in citas_existentes]
            
            # Filtramos comparando contra la propiedad "hora" del objeto
            resultado = [h for h in horas_disponibles if h["hora"] not in citas_formateadas]

            return Response(resultado, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

# 3. RESERVAR CITA (Nombre exacto para que urls.py no falle)
class ReservarCita(APIView):
    def post(self, request):
        data = request.data
        print(f"DEBUG DATA RECIBIDA: {data}") # 🔍 Esto te dirá qué está llegando

        try:
            # Extraemos con valores por defecto para evitar errores de None
            fecha = data.get('fecha')
            # Intentamos obtener hora_db, si no, probamos con 'hora'
            hora = data.get('hora_db') or data.get('hora')
            barbero_id = data.get('barberoId')
            cliente_id = data.get('cedula_cliente') or data.get('clienteId')

            if not all([fecha, hora, barbero_id, cliente_id]):
                return Response({"error": "Faltan campos obligatorios en el formulario"}, status=400)

            nueva_cita = Cita.objects.create(
                fecha=fecha,
                hora=hora,
                cedula_barbero_id=str(barbero_id),
                cedula_cliente_id=str(cliente_id),
                id_servicio=data.get('id_servicio', 1)
            )
            
            return Response({"message": "Cita agendada"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"ERROR AL GUARDAR: {str(e)}") # 🚨 Mira este error en tu consola negra
            return Response({"error": f"Error en base de datos: {str(e)}"}, status=400)
# 4. MI AGENDA (Para el barbero)
class AgendaDelBarberoView(APIView):
    def get(self, request):
        try:
            barbero_id = request.query_params.get('barberoId') 
            fecha = request.query_params.get('fecha')

            if not barbero_id or not fecha:
                return Response({"error": "Faltan parámetros barberoId o fecha"}, status=400)

            # 🚨 REGLA DE ORO: 
            # 1. Usamos str() para que Postgres no se queje (character varying = integer).
            # 2. Asegúrate que el nombre del campo sea cedula_barbero_id (como en tu modelo).
            citas = Cita.objects.filter(
                cedula_barbero_id=str(barbero_id), 
                fecha=fecha
            ).order_by('hora')

            serializer = CitaSerializer(citas, many=True)
            return Response(serializer.data)

        except Exception as e:
            # 🔍 Esto imprimirá el error real en tu consola negra de Django
            print(f"Error real en Mi Agenda: {str(e)}")
            return Response({"error": "Error interno del servidor", "detalle": str(e)}, status=500)