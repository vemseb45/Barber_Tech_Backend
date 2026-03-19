from django.contrib import admin
from barberias.models import Barberia, Especialidad


@admin.register(Barberia)
class BarberiaAdmin(admin.ModelAdmin):
    list_display = ("id_barberia", "nombre", "telefono", "email")
    search_fields = ("nombre",)


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("id_especialidad", "nombre")
    search_fields = ("nombre",)