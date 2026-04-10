# calificacion/serializers.py
from rest_framework import serializers
from .models import Calificacion

class CalificacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calificacion
        fields = '__all__'

    def validate_puntuacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La puntuación debe estar entre 1 y 5.")
        return value