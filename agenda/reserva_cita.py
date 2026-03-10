# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework.exceptions import ValidationError
from .services import reservar_cita  # Importamos la función

class ReservarCitaView(APIView):
    def post(self, request):
        data = request.data

        try:
            # Convertir strings de fecha y hora a objetos datetime/time
            fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(data['hora'], '%H:%M:%S').time()
            duracion = int(data['duracion'])
            id_servicio = int(data['id_servicio'])

            # Llamada a tu función
            cita = reservar_cita(
                barbero_cedula=data['cedula_barbero'],
                cliente_cedula=data['cedula_cliente'],
                fecha=fecha,
                hora_inicio=hora_inicio,
                duracion_servicio=duracion,
                id_servicio=id_servicio
            )

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Faltan campos obligatorios'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Respuesta exitosa
        return Response({
            'id': cita.id_cita,
            'fecha': str(cita.fecha),
            'hora': str(cita.hora),
            'cedula_cliente': cita.cedula_cliente_id,
            'cedula_barbero': cita.cedula_barbero_id,
            'id_servicio': cita.id_servicio
        }, status=status.HTTP_201_CREATED)