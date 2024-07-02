from django.db import models
from .usuario import User


class Notificacion(models.Model):
    usuario = models.ForeignKey(User, related_name="notificaciones", on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.tipo} - {self.texto[:20]}... ({self.fecha})'