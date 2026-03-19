from django.core.exceptions import ObjectDoesNotExist
from servicios.models.servicio import Servicio


class ServicioService:

 
    @staticmethod
    def obtener_servicio(id_servicio: int) -> Servicio:
        try:
            return Servicio.objects.select_related(
                "barberia",
                "especialidad"
            ).get(id_servicio=id_servicio)

        except ObjectDoesNotExist:
            raise ValueError("El servicio no existe")

    # ===============================
    # DURACIÓN (CRÍTICO PARA AGENDA)
    # ===============================
    @staticmethod
    def obtener_duracion(id_servicio: int) -> int:
        servicio = ServicioService.obtener_servicio(id_servicio)
        return servicio.duracion_minutos

    # ===============================
    # CREAR SERVICIO
    # ===============================
    @staticmethod
    def crear_servicio(serializer):
        return serializer.save()

    # ===============================
    # LISTAR SERVICIOS
    # ===============================
    @staticmethod
    def listar_servicios():
        return Servicio.objects.select_related(
            "barberia",
            "especialidad"
        ).all()