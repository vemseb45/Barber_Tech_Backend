from rest_framework import serializers
from barberos.models.barbero_detalle import BarberoDetalle


class BarberoDetalleSerializer(serializers.ModelSerializer):

    cedula = serializers.CharField(source="cedula.cedula", read_only=True)
    username = serializers.CharField(source="cedula.username", read_only=True)
    nombre = serializers.CharField(source="cedula.first_name", read_only=True)
    apellido = serializers.CharField(source="cedula.last_name", read_only=True)

    barberia = serializers.CharField(source="barberia.nombre", read_only=True)
    especialidad = serializers.CharField(source="especialidad.nombre", read_only=True)

    class Meta:
        model = BarberoDetalle
        fields = [
            "cedula",
            "username",
            "nombre",
            "apellido",
            "barberia",
            "especialidad",
        ]