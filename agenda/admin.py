from django.contrib import admin
from .models import AgendaBarbero


@admin.register(AgendaBarbero)
class AgendaBarberoAdmin(admin.ModelAdmin):

    # 🔥 Columnas que se ven en el admin
    list_display = (
        'id',
        'cedula_barbero',
        'dia',
        'hora_inicio',
        'hora_fin',
        'horario_legible'
    )

    # 🔍 Filtros laterales
    list_filter = (
        'dia',
        'cedula_barbero'
    )

    # 🔎 Buscador
    search_fields = (
        'cedula_barbero',
        'dia'
    )

    # 📊 Orden
    ordering = ('cedula_barbero', 'dia')

    # ✏️ Campos editables directamente en lista
    list_editable = ('hora_inicio', 'hora_fin')

    # 📄 Cantidad por página
    list_per_page = 20

    # 🔒 Campos de solo lectura
    readonly_fields = ('horario_legible',)

    # 🎨 Método personalizado (más PRO visual)
    def horario_legible(self, obj):
        return f"{obj.hora_inicio.strftime('%I:%M %p')} - {obj.hora_fin.strftime('%I:%M %p')}"
    
    horario_legible.short_description = "Horario"
