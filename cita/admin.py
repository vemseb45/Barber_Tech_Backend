from django.contrib import admin
from .models import Cita
from django.utils.html import format_html


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):

    # 🔥 Columnas visibles
    list_display = (
        'id',
        'cliente',
        'barbero',
        'servicio',
        'fecha',
        'hora_formateada',
        'estado_coloreado'
    )

    # 🔍 Filtros
    list_filter = (
        'estado',
        'fecha',
        'cedula_barbero',
        'servicio'
    )

    # 🔎 Buscador
    search_fields = (
        'cedula_cliente__username',
        'cedula_barbero__username',
        'servicio__nombre'
    )

    # 📊 Orden
    ordering = ('-fecha', '-hora')

    # 📄 Paginación
    list_per_page = 20

    # ⚡ Select related (optimización)
    list_select_related = (
        'cedula_cliente',
        'cedula_barbero',
        'servicio'
    )

    # 🧾 Solo lectura
    readonly_fields = ('hora_formateada',)

    # ======================================================
    # 🎨 CAMPOS PERSONALIZADOS
    # ======================================================

    def cliente(self, obj):
        return obj.cedula_cliente.username
    cliente.short_description = "Cliente"

    def barbero(self, obj):
        return obj.cedula_barbero.username
    barbero.short_description = "Barbero"

    def hora_formateada(self, obj):
        return obj.hora.strftime('%I:%M %p')
    hora_formateada.short_description = "Hora"

    # 🔥 Estado con colores PRO
    def estado_coloreado(self, obj):
        colores = {
            'PENT': 'orange',
            'CONF': 'green',
            'CANC': 'red'
        }

        nombres = {
            'PENT': 'Pendiente',
            'CONF': 'Confirmada',
            'CANC': 'Cancelada'
        }

        color = colores.get(obj.estado, 'gray')
        nombre = nombres.get(obj.estado, obj.estado)

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            nombre
        )

    estado_coloreado.short_description = "Estado"

    # ======================================================
    # ⚡ ACCIONES RÁPIDAS (MUY PRO)
    # ======================================================

    actions = ['confirmar_citas', 'cancelar_citas']

    def confirmar_citas(self, request, queryset):
        updated = queryset.update(estado='CONF')
        self.message_user(request, f"{updated} citas confirmadas correctamente.")
    confirmar_citas.short_description = "✅ Confirmar citas seleccionadas"

    def cancelar_citas(self, request, queryset):
        updated = queryset.update(estado='CANC')
        self.message_user(request, f"{updated} citas canceladas.")
    cancelar_citas.short_description = "❌ Cancelar citas seleccionadas"
