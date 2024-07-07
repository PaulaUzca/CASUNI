from casuni.models import Notificacion
from django.utils import timezone

def send_notification(user, message, tipo):
    notification = Notificacion(
        usuario=user,
        texto=message,
        tipo=tipo,
    )
    notification.save()