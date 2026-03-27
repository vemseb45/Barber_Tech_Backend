from django.urls import path
from .views import ReservarCita, finalizar_cita, HistorialCitasView, cancelar_cita

urlpatterns = [
    path('reservar/', ReservarCita.as_view()),
    path('finalizar/<int:cita_id>/', finalizar_cita),
    path('historial/', HistorialCitasView.as_view()),
    path('cancelar/<int:cita_id>/', cancelar_cita),
]