from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from usuarios.models.usuario import Usuario
from barberos.models.barbero_detalle import BarberoDetalle
from barberos.serializers.barbero_detalle_serializer import BarberoDetalleSerializer
from barberias.models.barberia import Barberia
from barberias.models.especialidad import Especialidad


class BarberoDetalleViewSet(ModelViewSet):
    queryset = BarberoDetalle.objects.all()
    serializer_class = BarberoDetalleSerializer

    @action(detail=False, methods=['post'], url_path='crear-barbero')
    def crear_barbero(self, request):
        try:
            data = request.data

            # 1. Crear usuario
            user = Usuario.objects.create(
                username=data["username"],
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
                email=data.get("email", ""),
                cedula=data["cedula"],
                telefono=data.get("telefono", ""),
                rol="Barbero"
            )
            user.set_password(data["password"])
            user.save()

            # 2. Obtener barbería y especialidad
            barberia = Barberia.objects.get(id_barberia=data["barberia_id"])
            especialidad = Especialidad.objects.get(id_especialidad=data["especialidad_id"])

            # 3. Crear detalle
            BarberoDetalle.objects.create(
                cedula=user,
                barberia=barberia,
                especialidad=especialidad
            )

            return Response({
                "success": True,
                "message": "Barbero creado correctamente"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)