# serializers.py
from rest_framework import serializers
from .models import Cita

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ['id', 'fecha', 'hora', 'cedula_cliente', 'cedula_barbero', 'id_servicio']