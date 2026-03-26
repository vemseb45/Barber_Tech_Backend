from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cita
from .serializers import CitaSerializer
from rest_framework import status
from rest_framework.decorators import api_view


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
        barbero = request.query_params.get("barberoId")

        if not barbero:
            return Response({
                "success": False,
                "message": "Falta barberoId"
            }, status=400)

        # 🔥 SOLO CITAS PENDIENTES
        citas = Cita.objects.filter(
            cedula_barbero_id=barbero,
            estado='PENT'
        )

        serializer = CitaSerializer(citas, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })


@api_view(['PATCH'])
def finalizar_cita(request, cita_id):
    try:
        cita = Cita.objects.get(id=cita_id)

        # 🔥 Cambiar estado a CONFIRMADA
        cita.estado = 'CONF'
        cita.save()

        return Response({
            "success": True,
            "message": "Cita finalizada correctamente"
        })

    except Cita.DoesNotExist:
        return Response({
            "success": False,
            "message": "Cita no encontrada"
        }, status=404)


class HistorialCitasView(APIView):
    def get(self, request):
        barbero_id = request.query_params.get("barberoId")

        if not barbero_id:
            return Response({
                "success": False,
                "message": "Falta barberoId"
            }, status=400)

        # 🔥 SOLO CONFIRMADAS (historial)
        citas = Cita.objects.filter(
            cedula_barbero_id=barbero_id,
            estado='CONF'
        ).select_related('servicio', 'cedula_cliente')

        data = []
        for cita in citas:
            data.append({
                "id": cita.id,
                "cliente": str(cita.cedula_cliente),
                "servicio": cita.servicio.nombre,
                "fecha": str(cita.fecha),
                "hora": cita.hora.strftime('%H:%M'),
                "precio": float(cita.servicio.precio),
            })

        return Response({
            "success": True,
            "data": data
        })