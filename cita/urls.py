from django.urls import path
from .views import ReservarCita

urlpatterns = [
    path('reservar/', ReservarCita.as_view()),
]