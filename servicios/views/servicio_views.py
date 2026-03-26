from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend

from servicios.models.servicio import Servicio
from servicios.serializers.servicio_serializer import ServicioSerializer
from servicios.permissions.servicio_permissions import IsAdminServicio
from servicios.services.servicio_service import ServicioService
from usuarios.utils.api_response import api_response


class ServicioViewSet(ModelViewSet):

    queryset = Servicio.objects.select_related(
        "barberia",
        "especialidad"
    ).all()

    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]

    # ======================
    # FILTROS PRO
    # ======================

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["barberia", "especialidad"]

    search_fields = [
        "nombre",
        "descripcion",
    ]

    ordering_fields = [
        "precio",
        "duracion_minutos",
        "nombre",
    ]

    ordering = ["nombre"]

    # ======================
    # LISTAR
    # ======================

    def list(self, request, *args, **kwargs):
        try:
            # 1. Obtenemos los servicios desde el service
            queryset = ServicioService.listar_servicios()
            
            # 2. Aplicamos filtros (búsqueda, orden, etc.)
            queryset = self.filter_queryset(queryset)

            # 3. Serializamos los datos (sin paginación para evitar el error)
            serializer = self.get_serializer(queryset, many=True)

            # 4. Retornamos con tu formato estándar
            return api_response(
                True,
                "Servicios obtenidos correctamente",
                serializer.data,
                status.HTTP_200_OK
            )
        except Exception as e:
            return api_response(False, str(e), None, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ======================
    # CREAR (solo admin)
    # ======================

    def create(self, request):

        if request.user.rol != "Admin":
            return api_response(False, "No autorizado", None, 403)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            servicio = ServicioService.crear_servicio(serializer)

            return api_response(
                True,
                "Servicio creado correctamente",
                self.get_serializer(servicio).data,
                status.HTTP_201_CREATED,
            )

        return api_response(False, "Error", serializer.errors, 400)

    # ======================
    # EDITAR
    # ======================

    def update(self, request, *args, **kwargs):

        if request.user.rol != "Admin":
            return api_response(False, "No autorizado", None, 403)

        return super().update(request, *args, **kwargs)

    # ======================
    # ELIMINAR
    # ======================

    def destroy(self, request, *args, **kwargs):

        if request.user.rol != "Admin":
            return api_response(False, "No autorizado", None, 403)

        return super().destroy(request, *args, **kwargs)