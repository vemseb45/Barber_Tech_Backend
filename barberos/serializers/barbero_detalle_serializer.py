from rest_framework import serializers
from barberos.models.barbero_detalle import BarberoDetalle


class BarberoDetalleSerializer(serializers.ModelSerializer):

    class Meta:
        model = BarberoDetalle
        fields = "__all__"