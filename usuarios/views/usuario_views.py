from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from ..models.usuario import Usuario
from ..serializers.usuario_serializer import UsuarioSerializer
from ..permissions.role_permissions import IsAdminRole
from ..utils.api_response import api_response


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