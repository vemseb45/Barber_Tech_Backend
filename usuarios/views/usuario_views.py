from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from ..models.usuario import Usuario
from ..serializers.usuario_serializer import UsuarioSerializer
from ..permissions.role_permissions import IsAdminRole
from ..utils.api_response import api_response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class UsuarioViewSet(ModelViewSet):

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminRole]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return api_response(
                True,
                "Usuario creado correctamente",
                serializer.data,
                status.HTTP_201_CREATED
            )

        return api_response(
            False,
            "Error en los datos enviados",
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['patch'])
    def cambiar_rol(self, request, pk=None):
        usuario = self.get_object() # Obtiene el usuario según el ID de la URL
        nuevo_rol = request.data.get('rol')

        # Validamos que el rol sea uno de los permitidos en tu modelo
        roles_permitidos = ['Admin', 'Barbero', 'Cliente']
        
        if nuevo_rol in roles_permitidos:
            usuario.rol = nuevo_rol
            usuario.save()
            return api_response(
                True,
                f"Rol actualizado a {nuevo_rol} correctamente",
                {"id": usuario.id, "username": usuario.username, "rol": usuario.rol},
                status.HTTP_200_OK
            )
        
        return api_response(
            False,
            "Rol no válido o no proporcionado",
            None,
            status.HTTP_400_BAD_REQUEST
        )
class ListaBarberosView(APIView):
    permission_classes = [AllowAny] # O IsAuthenticated si quieres que solo logueados vean barberos

    def get(self, request):
        # Filtramos por el rol que definiste en el modelo
        barberos = Usuario.objects.filter(rol='Barbero', estado='Activo')
        serializer = UsuarioSerializer(barberos, many=True)
        return api_response(True, "Lista de barberos", serializer.data)