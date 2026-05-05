from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from ..models import Usuario, PasswordResetToken

class SolicitarResetPassword(APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=404)

        token = PasswordResetToken.objects.create(usuario=usuario)

        reset_link = f"http://localhost:5173/reset-password?token={token.token}"

        send_mail(
            subject="Recuperar contraseña",
            message=f"Usa este link para cambiar tu contraseña: {reset_link}",
            from_email="tuemail@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "Correo enviado"})


class ResetPassword(APIView):
    def post(self, request):
        token = request.data.get("token")
        nueva_password = request.data.get("password")

        try:
            reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Token inválido"}, status=400)

        if not reset_token.is_valid():
            return Response({"error": "Token expirado"}, status=400)

        usuario = reset_token.usuario
        usuario.password = make_password(nueva_password)
        usuario.save()

        reset_token.delete()

        return Response({"message": "Contraseña actualizada"})