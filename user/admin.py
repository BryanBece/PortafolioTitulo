from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

      
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['id','email', 'tipoUsuario','nombre', 'apellido','is_staff', 'is_superuser']
    search_fields = ['email','tipoUsuario' 'nombre', 'apellido']
    fieldsets = (
        (None, {'fields': ('username','email', 'password', 'tipoUsuario')}),
        ('Información personal', {'fields': ('nombre', 'apellido')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'apellido', 'password1', 'password2', 'is_staff', 'is_superuser')
        }),
    )
    ordering = ['email']

@admin.register(Log)
class LogInicioSesionAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'fecha_inicio', 'texto']


@admin.register(tipo_usuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_tipo_usuario']
    search_fields = ['nombre_tipo_usuario']
