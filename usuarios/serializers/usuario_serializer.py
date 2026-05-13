from rest_framework import serializers
from ..models.usuario import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Es mejor listar los campos explícitamente para evitar enviar el hash del password
        fields = [
        'id',
        'username',
        'first_name',
        'last_name',
        'email', 
        'rol', 
        'cedula', 
        'telefono', 
        'estado', 
        'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('username'):
            ret['username'] = ret['username'].title()
        if ret.get('first_name'):
            ret['first_name'] = ret['first_name'].title()
        if ret.get('last_name'):
            ret['last_name'] = ret['last_name'].title()
        return ret

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user
