from django.contrib import admin
from .models.barbero_detalle import BarberoDetalle


@admin.register(BarberoDetalle)
class BarberoDetalleAdmin(admin.ModelAdmin):
    list_display = ("get_cedula", "get_username", "barberia", "especialidad")
    list_filter = ("barberia", "especialidad")
    search_fields = ("cedula__cedula", "cedula__username")

    def get_cedula(self, obj):
        return obj.cedula.cedula

    get_cedula.short_description = "Cédula"

    def get_username(self, obj):
        return obj.cedula.username

    get_username.short_description = "Usuario"