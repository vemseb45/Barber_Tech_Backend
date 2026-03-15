from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Credenciales inválidas.")
        else:
            raise serializers.ValidationError("Debe incluir usuario y contraseña.")

        data['user'] = user
        data['rol'] = user.rol
        return data



        