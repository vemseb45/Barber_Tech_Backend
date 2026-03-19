from rest_framework import serializers
from barberias.models import Especialidad


class EspecialidadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidad
        fields = [
            "id_especialidad",
            "nombre",
        ]