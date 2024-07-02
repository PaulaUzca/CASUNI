from django.db import models
from .usuario import Estudiante
from .alojamiento import Alojamiento

class Reserva(models.Model):
    estudiante = models.ForeignKey(Estudiante, related_name="reservas", on_delete=models.DO_NOTHING)
    alojamiento = models.ForeignKey(Alojamiento, related_name="reservas", on_delete=models.DO_NOTHING)

    fecha = models.DateTimeField(auto_now_add=True)
    fechaInicio = models.DateTimeField()
    fechaFin = models.DateTimeField()
    estado = estado = models.CharField(max_length=100)
    texto = models.TextField()