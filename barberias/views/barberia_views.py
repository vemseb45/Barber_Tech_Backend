from rest_framework import viewsets
from barberias.models import Barberia
from barberias.serializers.barberia_serializer import BarberiaSerializer


class BarberiaViewSet(viewsets.ModelViewSet):

    queryset = Barberia.objects.all()
    serializer_class = BarberiaSerializer