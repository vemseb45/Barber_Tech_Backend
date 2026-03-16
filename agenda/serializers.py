from rest_framework import serializers
from .models import Usuario, Cita

class BarberoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'rol']

class CitaSerializer(serializers.ModelSerializer):
    # Campos calculados para que la UI se vea bonita
    cliente = serializers.SerializerMethodField()
    hora_formateada = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        # 🚨 CAMBIO: 'id' en lugar de 'id_cita' para que coincida con el modelo
        # 🚨 CAMBIO: Incluimos 'cedula_cliente_id' y 'hora' para que React los encuentre
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
        # Como cedula_cliente_id es un string, buscamos al usuario en la DB
        try:
            # Buscamos al usuario por su ID (cédula)
            usuario = Usuario.objects.get(id=obj.cedula_cliente_id)
            return f"{usuario.username}" # O usuario.first_name si lo tienes
        except Usuario.DoesNotExist:
            return f"Cliente {obj.cedula_cliente_id}"

    def get_hora_formateada(self, obj):
        # Formato 12 horas (ej: 03:00 PM)
        return obj.hora.strftime('%I:%M %p')