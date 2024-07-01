from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    identificacion = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    edad = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    notificaciones = models.ManyToManyField(Notificacion)

    class Meta:
    abstract = True