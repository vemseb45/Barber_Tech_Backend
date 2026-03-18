from django.core.management.base import BaseCommand
from usuarios.models.usuario import Usuario


class Command(BaseCommand):
    help = "Inserta datos iniciales en la base de datos"

    def handle(self, *args, **kwargs):

        self.stdout.write("��� Insertando usuarios demo...")

        usuarios = [
            {
                "username": "camilo.sanchez",
                "password": "Admin123*",
                "rol": "Admin",
                "cedula": "1001",
                "telefono": "3001111111"
            },
            {
                "username": "manuel",
                "password": "Barbero123*",
                "rol": "Barbero",
                "cedula": "2001",
                "telefono": "3002222222"
            },
            {
                "username": "sebastian",
                "password": "Cliente123*",
                "rol": "Cliente",
                "cedula": "3001",
                "telefono": "3003333333"
            },
        ]

        for data in usuarios:

            if not Usuario.objects.filter(username=data["username"]).exists():

                user = Usuario(
                    username=data["username"],
                    rol=data["rol"],
                    cedula=data["cedula"],
                    telefono=data["telefono"],
                )

                user.set_password(data["password"])
                user.save()

                self.stdout.write(self.style.SUCCESS(
                    f"✔ Usuario creado: {user.username}"
                ))

        self.stdout.write(self.style.SUCCESS("✅ Seed completado"))
