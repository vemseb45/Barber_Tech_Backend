from django.urls import path
from .views import ListaBarberosView, DisponibilidadBarbero, ReservarCita, AgendaDelBarberoView

urlpatterns = [
    path('barberos/', ListaBarberosView.as_view(), name='lista-barberos'),
    path('disponibilidad/', DisponibilidadBarbero.as_view(), name='disponibilidad'),
    path('reservar/', ReservarCita.as_view(), name='reservar-cita'),
    path('miAgenda/', AgendaDelBarberoView.as_view(), name='agenda-barbero'),
]