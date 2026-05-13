from rest_framework import serializers
from .models import Cita
from usuarios.models import Usuario

class CitaSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar el nombre en el frontend
    cliente_nombre = serializers.SerializerMethodField(read_only=True)
    barbero_nombre = serializers.SerializerMethodField(read_only=True)
    servicio_nombre = serializers.SerializerMethodField(read_only=True)
    servicio_precio = serializers.SerializerMethodField(read_only=True)

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
            'cliente_nombre',
            'barbero_nombre',
            'servicio_nombre',
            'servicio_precio'
        ]

    def get_cliente_nombre(self, obj):
        if obj.cedula_cliente:
            return obj.cedula_cliente.username.title()
        return "Desconocido"

    def get_barbero_nombre(self, obj):
        if obj.cedula_barbero:
            return obj.cedula_barbero.username.title()
        return "Desconocido"

    def get_servicio_nombre(self, obj):
        if obj.servicio:
            return obj.servicio.nombre.title()
        return "Desconocido"

    def get_servicio_precio(self, obj):
        if obj.servicio:
            return obj.servicio.precio
        return 0