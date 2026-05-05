from django.urls import path
from .views import DisponibilidadBarbero, GestionarAgendaView, MiAgendaView, CargaMasivaAgendaView, AgendaDetalleView

urlpatterns = [
    path('disponibilidad/', DisponibilidadBarbero.as_view()),
    path('configurar/', GestionarAgendaView.as_view()),  # POST
    path('', GestionarAgendaView.as_view()),             # GET
    path('configurar/<int:id>/', AgendaDetalleView.as_view()),  # PUT / DELETE
    path('miAgenda/', MiAgendaView.as_view()),
    path('carga-masiva/', CargaMasivaAgendaView.as_view()),
]