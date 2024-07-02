from django.db import models
from .alojamiento import Alojamiento

class FotoAlojamiento(models.Model):
    alojamiento = models.ForeignKey(Alojamiento, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='alojamientos/')
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Foto de {self.alojamiento.nombre} - {self.descripcion[:20]}'
