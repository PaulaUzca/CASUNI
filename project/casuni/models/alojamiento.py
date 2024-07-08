from django.db import models
from .usuario import Propietario

class Alojamiento(models.Model):
    nombre = models.CharField(max_length=255)
    disponible = models.BooleanField(default=True)
    direccion = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.FloatField()
    servicios = models.ManyToManyField('Servicio', related_name='alojamientos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    fecha_publicacion = models.DateField(auto_now_add=True)
    
    propietario = models.ForeignKey(Propietario, related_name="propiedades", on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


