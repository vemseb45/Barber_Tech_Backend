from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cita
from .serializers import CitaSerializer
from rest_framework import status

class ReservarCita(APIView):
    def post(self, request):
        serializer = CitaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "Cita creada con éxito"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class AgendaDelBarberoView(APIView):
    def get(self, request):
        # Lista de citas ya reservadas para un barbero
        barbero = request.query_params.get("barberoId")
        citas = Cita.objects.filter(cedula_barbero_id=barbero)
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data)