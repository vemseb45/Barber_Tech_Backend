from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from usuarios.serializers.usuario_serializer import UsuarioSerializer
from usuarios.serializers.auth_serializer import LoginSerializer
from usuarios.utils.api_response import api_response

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return api_response(
                True,
                "Inicio de sesión exitoso",
                {
                    'token': str(refresh.access_token),
                    'user': {
                        'username': user.username,
                        'rol': user.rol
                    }
                },
                status.HTTP_200_OK
            )
        
        return api_response(
            False,
            "Credenciales inválidas",
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )

class MeView(APIView):
    # Este es el endpoint que usa el token para saber quién eres
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user contiene al usuario identificado por el token
        serializer = UsuarioSerializer(request.user)
        return api_response(
            True,
            "Datos del usuario obtenidos",
            serializer.data,
            status.HTTP_200_OK
        )

class RegistroView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(rol="Cliente")
            return api_response(True, "Usuario registrado correctamente", serializer.data, status.HTTP_201_CREATED)
        return api_response(False, "Error en el registro", serializer.errors, status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return api_response(True, "Sesión cerrada correctamente", {}, status.HTTP_200_OK)
        except Exception:
            return api_response(False, "Token inválido", {}, status.HTTP_400_BAD_REQUEST)