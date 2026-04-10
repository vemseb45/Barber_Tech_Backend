import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

class PasswordResetToken(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    creado = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.creado + timedelta(hours=1)