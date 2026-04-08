from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta

from .models import AgendaBarbero
from cita.models import Cita  
from usuarios.models.usuario import Usuario
from .serializers import BarberoSerializer, CitaSerializer, AgendaBarberoSerializer

class MiAgendaView(APIView):
    def get(self, request):
        barbero_id = request.query_params.get("barberoId")
        fecha = request.query_params.get("fecha")

        if not barbero_id or not fecha:
            return Response({
                "success": False,
                "message": "Faltan parámetros"
            }, status=400)

        try:
            citas = Cita.objects.filter(
                cedula_barbero_id=barbero_id,
                fecha=fecha
            )

            data = []
            for cita in citas:
                # 🔥 SOLO MOSTRAR PENDIENTES EN RESPUESTA (NO EN QUERY)
                if cita.estado != 'PENT':
                    continue

                data.append({
                    "id": cita.id,
                    "cedula_cliente_id": cita.cedula_cliente_id,
                    "fecha": str(cita.fecha),
                    "hora": cita.hora.strftime('%H:%M'),
                    "id_servicio": cita.servicio.id_servicio if hasattr(cita.servicio, 'id_servicio') else cita.servicio.id,
                    "estado": cita.estado
                })

            return Response({
                "success": True,
                "data": data
            })

        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=500)

class DisponibilidadBarbero(APIView):
    def get(self, request):
        barbero_id = request.query_params.get("barberoId")
        fecha_str = request.query_params.get("fecha")
        
        if not barbero_id or not fecha_str:
            return Response({"success": False, "message": "Faltan parámetros"}, status=400)

        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
            nombre_dia = dias[fecha_obj.weekday()]

            agenda = AgendaBarbero.objects.filter(
                cedula_barbero=barbero_id, 
                dia__iexact=nombre_dia
            ).first()

            if not agenda:
                return Response({
                    "success": True, 
                    "message": f"No hay agenda para el día {nombre_dia}", 
                    "data": [] 
                })
            
            # 1. Obtener horas ya reservadas
            citas_existentes = Cita.objects.filter(
                cedula_barbero_id=barbero_id, 
                fecha=fecha_obj
            ).values_list('hora', flat=True)

            # Convertimos a formato HH:MM para comparar fácilmente
            horas_ocupadas = [c.strftime('%H:%M') for c in citas_existentes]

            bloques = []
            hora_actual = datetime.combine(fecha_obj, agenda.hora_inicio)
            hora_fin = datetime.combine(fecha_obj, agenda.hora_fin)

            while hora_actual < hora_fin:
                hora_db_str = hora_actual.strftime('%H:%M')
                
                # 2. SOLO agregamos el bloque si NO está ocupado
                if hora_db_str not in horas_ocupadas:
                    bloques.append({
                        "hora": hora_actual.strftime('%I:%M %p'),
                        "hora_db": hora_actual.strftime('%H:%M:%S'),
                        "estado": "disponible"
                    })
                
                hora_actual += timedelta(minutes=30)

            return Response({
                "success": True,
                "message": "Lista de horas disponibles",
                "data": bloques
            })

        except Exception as e:
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
        cedula = request.data.get('cedula_barbero')
        dia = request.data.get('dia')
        
        instancia = AgendaBarbero.objects.filter(cedula_barbero=cedula, dia=dia).first()
        
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

class CargaMasivaAgendaView(APIView):
    def post(self, request):
        horarios = request.data.get("horarios", [])

        if not isinstance(horarios, list) or len(horarios) == 0:
            return Response({
                "success": False,
                "message": "No se enviaron datos válidos"
            }, status=400)

        errores = []
        creados = 0
        actualizados = 0

        for index, row in enumerate(horarios):
            try:
                cedula = row.get("cedula_barbero")
                dia = row.get("dia")
                hora_inicio = row.get("hora_inicio")
                hora_fin = row.get("hora_fin")

                # Validaciones básicas
                if not cedula or not dia or not hora_inicio or not hora_fin:
                    errores.append({
                        "fila": index + 2,
                        "error": "Campos incompletos"
                    })
                    continue

                # Convertir horas (string → time)
                try:
                    hora_inicio = datetime.strptime(hora_inicio, "%H:%M").time()
                    hora_fin = datetime.strptime(hora_fin, "%H:%M").time()
                except:
                    errores.append({
                        "fila": index + 2,
                        "error": "Formato de hora inválido (usa HH:MM)"
                    })
                    continue

                if hora_inicio >= hora_fin:
                    errores.append({
                        "fila": index + 2,
                        "error": "Hora inicio debe ser menor a hora fin"
                    })
                    continue

                # Buscar si ya existe
                agenda = AgendaBarbero.objects.filter(
                    cedula_barbero=cedula,
                    dia__iexact=dia
                ).first()

                if agenda:
                    agenda.hora_inicio = hora_inicio
                    agenda.hora_fin = hora_fin
                    agenda.save()
                    actualizados += 1
                else:
                    AgendaBarbero.objects.create(
                        cedula_barbero=cedula,
                        dia=dia,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin
                    )
                    creados += 1

            except Exception as e:
                errores.append({
                    "fila": index + 2,
                    "error": str(e)
                })

        return Response({
            "success": True,
            "message": "Proceso finalizado",
            "creados": creados,
            "actualizados": actualizados,
            "errores": errores
        })
class AgendaDetalleView(APIView):

    # 🔍 OBTENER UNO
    def get(self, request, id):
        try:
            agenda = AgendaBarbero.objects.get(id=id)
            serializer = AgendaBarberoSerializer(agenda)
            return Response({"success": True, "data": serializer.data})
        except AgendaBarbero.DoesNotExist:
            return Response({"success": False, "message": "No encontrado"}, status=404)

    # ✏️ ACTUALIZAR
    def put(self, request, id):
        try:
            agenda = AgendaBarbero.objects.get(id=id)
        except AgendaBarbero.DoesNotExist:
            return Response({"success": False, "message": "No encontrado"}, status=404)

        serializer = AgendaBarberoSerializer(agenda, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Horario actualizado",
                "data": serializer.data
            })

        return Response({"success": False, "errors": serializer.errors}, status=400)

    # 🗑 ELIMINAR
    def delete(self, request, id):
        try:
            agenda = AgendaBarbero.objects.get(id=id)
            agenda.delete()
            return Response({
                "success": True,
                "message": "Horario eliminado"
            })
        except AgendaBarbero.DoesNotExist:
            return Response({"success": False, "message": "No encontrado"}, status=404)