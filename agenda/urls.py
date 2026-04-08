from django.urls import path
from .views import DisponibilidadBarbero, GestionarAgendaView, MiAgendaView, CargaMasivaAgendaView, AgendaDetalleView

urlpatterns = [
    path('disponibilidad/', DisponibilidadBarbero.as_view()),
    path('configurar/', GestionarAgendaView.as_view()),  # POST (crear/actualizar por día)
    path('', GestionarAgendaView.as_view()),             # GET (listar)
    path('delet/<int:id>/', AgendaDetalleView.as_view()),      # 🔥 DELETE / PUT
    path('miAgenda/', MiAgendaView.as_view()),
    path('carga-masiva/', CargaMasivaAgendaView.as_view()),
]