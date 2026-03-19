from django.urls import path
from .views.auth_views import RegistroView, LogoutView, LoginView, MeView
from .views.usuario_views import UsuarioViewSet, ListaBarberosView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('barberos/', ListaBarberosView.as_view(), name='barberos-list'),
]

urlpatterns += router.urls