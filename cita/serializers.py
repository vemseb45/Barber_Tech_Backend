from rest_framework import serializers
from .models import Cita
from usuarios.models import Usuario

class CitaSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar el nombre en el frontend
    cliente_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cita
        # IMPORTANTE: Usa los nombres exactos de los atributos en tu modelo
        fields = [
            'id', 
            'fecha', 
            'hora', 
            'servicio', 
            'cedula_cliente',  # FK al modelo Usuario (Cliente)
            'cedula_barbero',  # FK al modelo Usuario (Barbero) - ¡ESTE FALTABA!
            'cliente_nombre'
        ]

    def get_cliente_nombre(self, obj):
        # obj.cedula_cliente es la instancia del usuario relacionado
        if obj.cedula_cliente:
            return obj.cedula_cliente.username
        return "Desconocido"