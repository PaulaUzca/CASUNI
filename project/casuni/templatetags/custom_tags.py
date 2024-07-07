from django import template
from datetime import datetime


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