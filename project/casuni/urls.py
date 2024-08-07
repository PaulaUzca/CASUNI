from django.urls import path
from . import views  # Import your views from the same app

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),    
    path('logout/', views.logout, name='logout'),    
    path('perfil/', views.perfil, name='perfil'), 
    path('notificaciones/', views.notifications, name='notificaciones'),    
    path('estudiante/perfil/<int:estudiante_id>/', views.estudiante_perfil, name='estudiante_perfil'),
    path('propietario/perfil/<int:propietario_id>/', views.propietario_perfil, name='propietario_perfil'),
    path('alojamiento/<int:alojamiento_id>/', views.alojamiento_detalle, name='alojamiento_detalle'),
    path('solicitud/<int:solicitud_id>', views.solicitud, name='solicitud'),
    path('solicitud/<int:id>/aceptar/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('solicitud/<int:id>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('solicitud/<int:solicitud_id>/crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('submit-question/', views.enviar_pregunta, name='submit_question'),
    path('answer_question/', views.answer_question, name='answer_question'),
    path('procesar_resena/', views.procesar_resena, name='procesar_resena'),
    path('vista_propietario/perfil/<int:propietario_id>/', views.vista_propietario_perfil, name='vista_propietario'),

]
