from rest_framework import viewsets
from barberias.models import Especialidad
from barberias.serializers.especialidad_serializer import EspecialidadSerializer


class EspecialidadViewSet(viewsets.ModelViewSet):

    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer