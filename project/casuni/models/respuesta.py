from django.db import models
from .pregunta import Pregunta

class Respuesta(models.Model):
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    pregunta = models.ForeignKey(Pregunta, related_name = "respuestas", on_delete=models.CASCADE)

