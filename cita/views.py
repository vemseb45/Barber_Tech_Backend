from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cita
from .serializers import CitaSerializer

class ReservarCita(APIView):
    def post(self, request):
        # Aquí va tu lógica de Cita.objects.create(...)
        return Response({"mensaje": "Cita creada con éxito"})

class AgendaDelBarberoView(APIView):
    def get(self, request):
        # Lista de citas ya reservadas para un barbero
        barbero = request.query_params.get("barberoId")
        citas = Cita.objects.filter(cedula_barbero_id=barbero)
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data)