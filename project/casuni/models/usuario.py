from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Extend the base user model for specific roles (e.g., Student and Proprietor)
class Estudiante(models.Model):

    telefono = models.CharField(max_length=20, blank=True, null=True)
    identificacion = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=250, blank=True)
    genero = models.CharField(max_length=20, blank=True, null=True, choices=[('F', 'Femenino'), ('M', 'Masculino'), ('B', 'No binario'), ("O", "Otro")])
    fecha_nacimiento = models.DateField(blank=True, null=True)    
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='perfiles/', default='perfiles/default_profile.jpg')
    universidad = models.TextField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="estudiante")

    def __str__(self):
        return self.user.username

class Propietario(models.Model):

    telefono = models.CharField(max_length=20, blank=True, null=True)
    identificacion = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=250, blank=True)
    genero = models.CharField(max_length=20, blank=True, null=True, choices=[('F', 'Femenino'), ('M', 'Masculino'), ('B', 'No binario'), ("O", "Otro")])
    fecha_nacimiento = models.DateField(blank=True, null=True)    
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='perfiles/', default='perfiles/default_profile.jpg')
    

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="propietario")

    def __str__(self):
        return self.user.username