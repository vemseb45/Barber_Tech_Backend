from rest_framework.viewsets import ModelViewSet
from barberos.models.barbero_detalle import BarberoDetalle
from barberos.serializers.barbero_detalle_serializer import BarberoDetalleSerializer


class BarberoDetalleViewSet(ModelViewSet):
    queryset = BarberoDetalle.objects.all()
    serializer_class = BarberoDetalleSerializer