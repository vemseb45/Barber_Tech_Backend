from rest_framework import serializers
# Importamos cada cosa de su nueva casa
from .models import AgendaBarbero
from cita.models import Cita 
from usuarios.models.usuario import Usuario 

class BarberoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'rol']

class CitaSerializer(serializers.ModelSerializer):
    cliente = serializers.SerializerMethodField()
    hora_formateada = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        fields = [
            'id', 
            'cliente', 
            'fecha', 
            'hora', 
            'hora_formateada', 
            'id_servicio', 
            'cedula_cliente_id'
        ]

    def get_cliente(self, obj):
        try:
            # Buscamos en el modelo de la app usuarios
            usuario = Usuario.objects.get(id=obj.cedula_cliente_id)
            return f"{usuario.username}"
        except (Usuario.DoesNotExist, ValueError):
            return f"Cliente {obj.cedula_cliente_id}"

    def get_hora_formateada(self, obj):
        return obj.hora.strftime('%I:%M %p') if obj.hora else None
    


class AgendaBarberoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaBarbero
        fields = ['id', 'cedula_barbero', 'dia', 'hora_inicio', 'hora_fin']

    def validate(self, data):
        if data['hora_inicio'] >= data['hora_fin']:
            raise serializers.ValidationError("La hora de inicio debe ser menor a la hora de fin.")
        return data