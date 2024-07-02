from django.db import models
from .usuario import Estudiante
from .alojamiento import Alojamiento 

class Pregunta(models.Model):
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    estudiante = models.ForeignKey(Estudiante, related_name="preguntas", on_delete=models.CASCADE)
    alojamiento = models.ForeignKey(Alojamiento, related_name="preguntas", on_delete=models.CASCADE)

