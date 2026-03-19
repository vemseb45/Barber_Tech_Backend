from rest_framework import serializers
from ..models.usuario import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Es mejor listar los campos explícitamente para evitar enviar el hash del password
        fields = ['id', 'username', 'email', 'rol', 'cedula', 'telefono', 'estado', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user
