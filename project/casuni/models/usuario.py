# Assuming you have already created a Django project and app

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Define a custom manager for the user model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Define a base user model
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    telefono = models.CharField(max_length=20, blank=True, null=True)
    identificacion = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField()
    genero = models.CharField(max_length=20, blank=True, null=True, choices=[('F', 'Femenino'), ('M', 'Masculino'), ('B', 'No binario'), ("O", "Otro")])
    fecha_nacimiento = models.DateField()    
    descripcion = models.TextField(blank=True)

    activo = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # Add additional fields as needed, such as first_name, last_name, etc.
    # Define any additional methods or properties specific to the base user model

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

# Extend the base user model for specific roles (e.g., Student and Proprietor)
class Estudiante(User):
    # Add additional fields specific to students
    universidad = models.TextField()

    class Meta:
        verbose_name = 'estudiante'
        verbose_name_plural = 'estudiantes'

class Propietario(User):
    # Add additional fields specific to proprietors

    class Meta:
        verbose_name = 'propietario'
        verbose_name_plural = 'propietarios'
