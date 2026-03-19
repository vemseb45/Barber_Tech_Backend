from django.urls import path
from .views import DisponibilidadBarbero, GestionarAgendaView

urlpatterns = [
    path('disponibilidad/', DisponibilidadBarbero.as_view(), name='disponibilidad'),
    path('configurar/', GestionarAgendaView.as_view(), name='configurar-agenda'),
]