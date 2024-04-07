from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Log

      
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['id','email', 'nombre', 'apellido','is_staff', 'is_superuser']
    search_fields = ['email', 'nombre', 'apellido']
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
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


