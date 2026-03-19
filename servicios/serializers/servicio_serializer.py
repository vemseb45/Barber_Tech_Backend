from rest_framework import serializers
from servicios.models.servicio import Servicio
from barberias.models import Barberia, Especialidad


# =============================
# Nested serializers (READ)
# =============================

class BarberiaNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barberia
        fields = ["id_barberia", "nombre"]


class EspecialidadNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ["id_especialidad", "nombre"]


# =============================
# MAIN SERIALIZER
# =============================

class ServicioSerializer(serializers.ModelSerializer):

    # WRITE (frontend envía IDs)
    barberia = serializers.PrimaryKeyRelatedField(
        queryset=Barberia.objects.all()
    )

    especialidad = serializers.PrimaryKeyRelatedField(
        queryset=Especialidad.objects.all()
    )

    # READ (frontend recibe objetos)
    barberia_detalle = BarberiaNestedSerializer(
        source="barberia",
        read_only=True
    )

    especialidad_detalle = EspecialidadNestedSerializer(
        source="especialidad",
        read_only=True
    )

    class Meta:
        model = Servicio
        fields = [
            "id_servicio",
            "nombre",
            "descripcion",
            "precio",
            "duracion_minutos",
            "barberia",
            "especialidad",
            "barberia_detalle",
            "especialidad_detalle",
        ]

    # =============================
    # VALIDACIONES
    # =============================

    def validate_duracion_minutos(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "La duración debe ser mayor a 0 minutos."
            )

        if value > 240:
            raise serializers.ValidationError(
                "La duración no puede superar 240 minutos."
            )

        return value

    def validate_precio(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "El precio debe ser mayor a 0."
            )

        return value