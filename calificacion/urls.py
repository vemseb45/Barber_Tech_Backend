from django.urls import path
from .views import CrearCalificacionView,PromedioBarberoView

urlpatterns = [
    path('crear/', CrearCalificacionView.as_view(), name='crear-calificacion'),
    path('promedio/<int:barbero_id>/', PromedioBarberoView.as_view()),
]