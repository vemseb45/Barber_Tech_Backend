from rest_framework.routers import DefaultRouter
from .views.servicio_views import ServicioViewSet

router = DefaultRouter()
router.register(r"servicios", ServicioViewSet, basename="servicios")

urlpatterns = router.urls