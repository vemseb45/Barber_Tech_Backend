from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Calificacion
from cita.models import Cita
from datetime import datetime
from django.db.models import Avg



class CrearCalificacionView(APIView):

    def post(self, request):
        id_cita = request.data.get('id_cita')
        puntuacion = request.data.get('puntuacion')
        comentario = request.data.get('comentario')

        try:
            cita = Cita.objects.get(id_cita=id_cita)
        except Cita.DoesNotExist:
            return Response({"error": "Cita no existe"}, status=404)

        # Validar que ya pasó
        if cita.fecha > datetime.now():
            return Response({"error": "La cita aún no ha terminado"}, status=400)

        # Validar que no exista
        if hasattr(cita, 'calificacion'):
            return Response({"error": "Ya fue calificada"}, status=400)

        calificacion = Calificacion.objects.create(
            cita=cita,
            puntuacion=puntuacion,
            comentario=comentario
        )

        return Response({"mensaje": "Calificación guardada"}, status=201)

class PromedioBarberoView(APIView):

    def get(self, request, barbero_id):
        promedio = Calificacion.objects.filter(
            cita__barbero_id=barbero_id
        ).aggregate(promedio=Avg('puntuacion'))

        return Response({
            "promedio": promedio["promedio"] or 0
        })