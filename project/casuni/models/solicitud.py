from django.db import models
from .usuario import Estudiante
from .alojamiento import Alojamiento 

class Solicitud(models.Model):
    estudiante = models.ForeignKey(Estudiante, related_name="solicitudes", on_delete=models.CASCADE)
    alojamiento = models.ForeignKey(Alojamiento, related_name = "solicitudes", on_delete=models.CASCADE)
    
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    fechaInicio = models.DateTimeField()
    fechaFin = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=[('P', 'Pendiente'), ('A', 'Aceptada'), ('R', 'Rechazada')])



