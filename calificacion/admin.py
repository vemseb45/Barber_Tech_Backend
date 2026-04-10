from django.contrib import admin
from .models import Calificacion

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = (
        'id_calificacion',
        'cita',
        'barbero',
        'puntuacion',
        'fecha'
    )

    list_filter = ('puntuacion', 'fecha')
    search_fields = (
        'cita__id_cita',
        'cita__barbero__nombre',
    )

    ordering = ('-fecha',)

    def barbero(self, obj):
        return obj.cita.cedula_barbero  # si tienes campo nombre
        barbero.short_description = "Barbero"