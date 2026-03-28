from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cita
from .serializers import CitaSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


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


@api_view(['PATCH'])
def cancelar_cita(request, cita_id):
    try:
        cita = Cita.objects.get(id=cita_id)

        if cita.estado != 'PENT':
            return Response({
                "success": False,
                "message": "Solo se pueden cancelar citas pendientes"
            }, status=400)

        cita.estado = 'CANC'
        cita.save()

        return Response({
            "success": True,
            "message": "Cita cancelada correctamente"
        })

    except Cita.DoesNotExist:
        return Response({
            "success": False,
            "message": "Cita no encontrada"
        }, status=404)


class HistorialCitasView(APIView):
    def get(self, request):
        barbero_id = request.query_params.get("barberoId")
        estado = request.query_params.get("estado")

        if not barbero_id:
            return Response({
                "success": False,
                "message": "Falta barberoId"
            }, status=400)

        filtros = {
            "cedula_barbero_id": barbero_id
        }

        if estado:
            filtros["estado"] = estado
        else:
            filtros["estado"] = 'CONF'

        citas = Cita.objects.filter(**filtros).select_related('servicio', 'cedula_cliente')

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


# ✅ ENDPOINT CORREGIDO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def citas_pendientes_cliente(request):
    try:
        cliente = request.user

        citas = Cita.objects.filter(
            cedula_cliente=cliente,
            estado='PENT'   # ✅ CORREGIDO
        ).order_by('fecha', 'hora')

        serializer = CitaSerializer(citas, many=True)

        return Response({
            "success": True,
            "data": serializer.data
        })

    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=400)