from django.contrib import admin
from servicios.models.servicio import Servicio


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):

    list_display = (
        "id_servicio",
        "nombre",
        "precio",
        "duracion_minutos",
        "barberia",
        "especialidad",
    )

    list_filter = ("barberia", "especialidad")

    search_fields = ("nombre",)