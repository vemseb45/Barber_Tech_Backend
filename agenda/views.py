from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta

# IMPORTACIONES CORRECTAS
from .models import AgendaBarbero
from cita.models import Cita  
from usuarios.models.usuario import Usuario
from .serializers import BarberoSerializer, CitaSerializer, AgendaBarberoSerializer

class DisponibilidadBarbero(APIView):
    def get(self, request):
        barbero_id = request.query_params.get("barberoId")
        fecha_str = request.query_params.get("fecha")
        
        if not barbero_id or not fecha_str:
            return Response({"success": False, "message": "Faltan parámetros"}, status=400)

        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            # 1. Definimos los días exactamente como suelen estar en las DBs (puedes probar con/sin acento)
            # Si en tu DB dice "Sabado", quítale el acento aquí:
            dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
            nombre_dia = dias[fecha_obj.weekday()]

            # 2. Usamos __iexact para que busque "Sabado" o "sabado" sin problemas
            agenda = AgendaBarbero.objects.filter(
                cedula_barbero=barbero_id, 
                dia__iexact=nombre_dia  # <--- iExact ignora mayúsculas/minúsculas
            ).first()

            if not agenda:
                # Esto te ayudará a ver qué intentó buscar Django en tu consola:
                print(f"DEBUG: Buscando horario para barbero {barbero_id} el dia {nombre_dia}")
                return Response({
                    "success": True, 
                    "message": f"No hay agenda para el día {nombre_dia}", 
                    "data": [] 
                })
            
    # ... resto del código de los bloques (el while) ...
            # 3. Corregimos el filtro de citas: usamos 'cedula_barbero_id' (o el que use tu modelo Cita)
            citas_existentes = Cita.objects.filter(
                cedula_barbero_id=barbero_id, 
                fecha=fecha_obj
            ).values_list('hora', flat=True)

            # 4. Generar bloques
            bloques = []
            hora_actual = datetime.combine(fecha_obj, agenda.hora_inicio)
            hora_fin = datetime.combine(fecha_obj, agenda.hora_fin)

            while hora_actual < hora_fin:
                hora_db = hora_actual.time()
                # Comparamos si la hora está en las citas existentes
                esta_ocupada = any(c.strftime('%H:%M') == hora_db.strftime('%H:%M') for c in citas_existentes)

                bloques.append({
                    "hora": hora_actual.strftime('%I:%M %p'),
                    "hora_db": hora_actual.strftime('%H:%M:%S'),
                    "disponible": not esta_ocupada
                })
                
                hora_actual += timedelta(minutes=30) # Bloques de 30 min

            return Response({
                "success": True,
                "message": "Lista de horas disponibles",
                "data": bloques
            })

        except Exception as e:
            # Esto te ayudará a ver errores exactos en la consola de Django
            import traceback
            print(traceback.format_exc())
            return Response({"success": False, "message": str(e)}, status=500)

class GestionarAgendaView(APIView):
    # Obtener todos los horarios (o filtrar por barbero)
    def get(self, request):
        barbero_id = request.query_params.get('barberoId')
        if barbero_id:
            agendas = AgendaBarbero.objects.filter(cedula_barbero=barbero_id)
        else:
            agendas = AgendaBarbero.objects.all()
        
        serializer = AgendaBarberoSerializer(agendas, many=True)
        return Response({"success": True, "data": serializer.data})

    # Crear o actualizar un horario
    def post(self, request):
        # Intentamos buscar si ya existe un horario para ese barbero ese día
        cedula = request.data.get('cedula_barbero')
        dia = request.data.get('dia')
        
        instancia = AgendaBarbero.objects.filter(cedula_barbero=cedula, dia=dia).first()
        
        # Si existe, actualizamos. Si no, creamos uno nuevo.
        serializer = AgendaBarberoSerializer(instancia, data=request.data) if instancia \
                     else AgendaBarberoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True, 
                "message": "Horario guardado correctamente",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)