from django.urls import path
from .views import DisponibilidadBarbero, ReservarCita

urlpatterns = [
    path('barberos/<str:cedula_barbero>/disponibilidad/', DisponibilidadBarbero.as_view(), name='disponibilidad-barbero'),
    path('citas/reservar/', ReservarCita.as_view(), name='reservar-cita'),
]