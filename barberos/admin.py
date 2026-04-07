from django.contrib import admin
from .models.barbero_detalle import BarberoDetalle


@admin.register(BarberoDetalle)
class BarberoDetalleAdmin(admin.ModelAdmin):
    list_display = ("cedula", "barberia", "especialidad")
    search_fields = ("cedula__nombre",)
    list_filter = ("barberia", "especialidad")