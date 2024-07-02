from django.db import models
from .reserva import Reserva

class Reseña(models.Model):
    reserva = models.ForeignKey(Reserva, related_name="reseñas", on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()
    calificacion = models.IntegerField()