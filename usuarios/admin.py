from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'cedula', 'rol', 'estado', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('cedula', 'telefono', 'rol', 'estado')
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)