from rest_framework import serializers
from barberias.models import Barberia


class BarberiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Barberia
        fields = [
            "id_barberia",
            "nombre",
            "direccion",
            "telefono",
            "email",
        ]