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
    path('solicitud/<int:alojamiento_id>/<int:solicitud_id>', views.solicitud, name='solicitud'),
]
