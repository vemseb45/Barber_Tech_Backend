# agenda/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from .models import Cita
from .serializers import CitaSerializer
from .utils.agenda import obtener_disponibilidad_opt

class DisponibilidadBarbero(APIView):
    def get(self, request, cedula_barbero):
        fecha_str = request.query_params.get('fecha')
        duracion = int(request.query_params.get('duracion', 30))

        if not fecha_str:
            return Response({'error': 'Se requiere la fecha'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Formato de fecha inválido'}, status=status.HTTP_400_BAD_REQUEST)

        disponibles = obtener_disponibilidad_opt(cedula_barbero, fecha, duracion)
        return Response({'disponibilidad': disponibles}, status=status.HTTP_200_OK)


class ReservarCita(APIView):
    def post(self, request):
        data = request.data
        cedula_barbero = data.get('cedula_barbero')
        cedula_cliente = data.get('cedula_cliente')
        fecha_str = data.get('fecha')
        hora_str = data.get('hora')
        duracion = int(data.get('duracion', 30))
        id_servicio = data.get('id_servicio')

        if not all([cedula_barbero, cedula_cliente, fecha_str, hora_str, id_servicio]):
            return Response({'error': 'Faltan campos requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(hora_str, '%H:%M:%S').time()
        except ValueError:
            return Response({'error': 'Formato de fecha u hora inválido'}, status=status.HTTP_400_BAD_REQUEST)

        disponibles = obtener_disponibilidad_opt(cedula_barbero, fecha, duracion)
        hora_fin = (datetime.combine(fecha, hora_inicio) + timedelta(minutes=duracion)).time()

        if (hora_inicio, hora_fin) not in disponibles:
            return Response({'error': 'Horario no disponible'}, status=status.HTTP_400_BAD_REQUEST)

        cita = Cita.objects.create(
            fecha=fecha,
            hora=hora_inicio,
            cedula_cliente_id=cedula_cliente,
            cedula_barbero_id=cedula_barbero,
            id_servicio=id_servicio
        )

        serializer = CitaSerializer(cita)
        return Response(serializer.data, status=status.HTTP_201_CREATED)