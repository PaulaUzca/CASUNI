from django import template
from datetime import datetime
from casuni.models import Reserva, Reseña
from django.db.models import Avg


register = template.Library()

@register.filter
def has_estudiante(user):
    return user.estudiante.exists()

@register.filter
def has_propietario(user):
    return user.propietario.exists()


@register.filter
def filter_pendiente(solicitudes):
    return solicitudes.filter(estado='P')

@register.filter
def tiene_pendiente(solicitudes):
    return solicitudes.filter(estado='P')



@register.filter
def reserva_activa(reserva):
    """
    Custom template filter to check if the reserva is active.
    Active if today's date is between fechaInicio and fechaFin.
    """
    today = datetime.now()
    return reserva.fechaInicio <= today <= reserva.fechaFin

@register.filter
def reservas_finalizada(reservas):
    return reservas.filter(estado ="Finalizada")


@register.simple_tag
def average_calificacion(alojamiento):
    # Calculate the average calificacion for Reservas associated with the given Alojamiento
    avg_calificacion = Reserva.objects.filter(alojamiento=alojamiento).aggregate(avg_calificacion=Avg('reseñas__calificacion'))['avg_calificacion']
    
    # Handle cases where there are no Reservas or no reseñas with calificacion
    if avg_calificacion is None:
        return "-"
    else:
        return round(avg_calificacion, 2)
    
@register.simple_tag
def count_reseñas(alojamiento):
    # Retrieve the count of Reseñas associated with the given Alojamiento
    return Reseña.objects.filter(reserva__alojamiento=alojamiento).count()