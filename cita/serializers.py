from rest_framework import serializers
from .models import Cita
from usuarios.models import Usuario

class CitaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        fields = ['id', 'fecha', 'hora', 'servicio', 'cedula_cliente_id', 'cliente_nombre']

    def get_cliente_nombre(self, obj):
        try:
            u = Usuario.objects.get(cedula=obj.cedula_cliente_id)
            return u.username
        except:
            return "Desconocido"