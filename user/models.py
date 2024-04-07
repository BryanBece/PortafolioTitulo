# Create your models here.
from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin
from django.utils import timezone

# Create your models here.

# Custom User Manager
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('El email debe ser obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe ser staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe ser superusuario')
        return self._create_user(email, password, **extra_fields)
    
# Usuario personalizado
class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def get_full_name(self):
        return f'{self.nombre} {self.apellido}'
    
    def get_short_name(self):
        return self.nombre or self.email.split('@')[0]
    

class Log(models.Model):
    username = models.CharField(max_length=150)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    texto = models.CharField(max_length=100, default="inicio de sesión")
    def __str__(self):
        return f"{self.username} - {self.fecha_inicio} - {self.texto}"