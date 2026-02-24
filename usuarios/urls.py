from django.urls import path
from .views.auth_views import RegistroView, LogoutView
from .views.usuario_views import UsuarioViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls