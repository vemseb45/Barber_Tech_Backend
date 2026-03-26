from django.urls import path
from .views import DisponibilidadBarbero, GestionarAgendaView, MiAgendaView

urlpatterns = [
    path('disponibilidad/', DisponibilidadBarbero.as_view(), name='disponibilidad'),
    path('configurar/', GestionarAgendaView.as_view(), name='configurar-agenda'),
    path('miAgenda/', MiAgendaView.as_view(), name='agendabarbero'),
]