from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from usuarios.models.usuario import Usuario
from barberos.models.barbero_detalle import BarberoDetalle
from barberos.serializers.barbero_detalle_serializer import BarberoDetalleSerializer
from barberias.models.barberia import Barberia
from barberias.models.especialidad import Especialidad
from django.db import transaction

class BarberoDetalleViewSet(ModelViewSet):
    queryset = BarberoDetalle.objects.all()
    serializer_class = BarberoDetalleSerializer

    @action(detail=False, methods=['post'], url_path='crear-barbero')
    def crear_barbero(self, request):
        data = request.data

        try:
            # 🔴 1. VALIDACIONES OBLIGATORIAS
            username = data.get("username")
            password = data.get("password")
            cedula = data.get("cedula")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email")

            if not username or not password or not cedula:
                return Response({
                    "success": False,
                    "message": "Username, password y cédula son obligatorios"
                }, status=status.HTTP_400_BAD_REQUEST)

            if not first_name or not last_name or not email:
                return Response({
                    "success": False,
                    "message": "Nombre, apellido y email son obligatorios"
                }, status=status.HTTP_400_BAD_REQUEST)

            # 🔴 2. VALIDAR DUPLICADOS
            if Usuario.objects.filter(username=username).exists():
                return Response({
                    "success": False,
                    "message": "El username ya existe"
                }, status=status.HTTP_400_BAD_REQUEST)

            if Usuario.objects.filter(cedula=cedula).exists():
                return Response({
                    "success": False,
                    "message": "La cédula ya existe"
                }, status=status.HTTP_400_BAD_REQUEST)

            # 🔴 3. VALIDAR IDS
            barberia_id = data.get("barberia_id")
            especialidad_id = data.get("especialidad_id")

            if not barberia_id or not especialidad_id:
                return Response({
                    "success": False,
                    "message": "Barbería y especialidad son obligatorias"
                }, status=status.HTTP_400_BAD_REQUEST)

            # 🔴 4. TRANSACCIÓN (CRÍTICO)
            with transaction.atomic():

                # Crear usuario
                user = Usuario.objects.create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    cedula=cedula,
                    telefono=data.get("telefono", ""),
                    rol="Barbero"
                )

                user.set_password(password)
                user.save()

                # Obtener relaciones
                barberia = Barberia.objects.get(id_barberia=barberia_id)
                especialidad = Especialidad.objects.get(id_especialidad=especialidad_id)

                # Crear detalle
                BarberoDetalle.objects.create(
                    cedula=user,
                    barberia=barberia,
                    especialidad=especialidad
                )

            return Response({
                "success": True,
                "message": "Barbero creado correctamente"
            }, status=status.HTTP_201_CREATED)

        except Barberia.DoesNotExist:
            return Response({
                "success": False,
                "message": "La barbería no existe"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Especialidad.DoesNotExist:
            return Response({
                "success": False,
                "message": "La especialidad no existe"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)