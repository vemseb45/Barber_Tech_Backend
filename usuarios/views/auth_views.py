from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.usuario_serializer import UsuarioSerializer
from ..utils.api_response import api_response


class RegistroView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(rol="Cliente")

            return api_response(
                True,
                "Usuario registrado correctamente",
                serializer.data,
                status.HTTP_201_CREATED
            )

        return api_response(
            False,
            "Error en el registro",
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return api_response(
                True,
                "Sesión cerrada correctamente",
                {},
                status.HTTP_200_OK
            )

        except Exception:
            return api_response(
                False,
                "Token inválido",
                {},
                status.HTTP_400_BAD_REQUEST
            )