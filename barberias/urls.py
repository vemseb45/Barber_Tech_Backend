from django.urls import path, include
from rest_framework.routers import DefaultRouter

from barberias.views.barberia_views import BarberiaViewSet
from barberias.views.especialidad_views import EspecialidadViewSet


router = DefaultRouter()
router.register(r"barberias", BarberiaViewSet, basename="barberias")
router.register(r"especialidades", EspecialidadViewSet, basename="especialidades")

urlpatterns = [
    path("", include(router.urls)),
]