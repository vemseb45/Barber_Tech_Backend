from rest_framework.routers import DefaultRouter
from .views.barbero_detalle_views import BarberoDetalleViewSet

router = DefaultRouter()
router.register(r"barberos", BarberoDetalleViewSet, basename="barberos")

urlpatterns = router.urls
