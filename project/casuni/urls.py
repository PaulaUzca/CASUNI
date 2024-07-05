from django.urls import path
from . import views  # Import your views from the same app

urlpatterns = [
    path('', views.home, name='home'),  # Example path for dashboard view
    path('login/', views.login_view, name='login'),      # Example path for login view
    path('estudiante/', views.estudiante_home, name='estudiante_home'),
    path('propietario/', views.propietario_home, name='propietario_home'),
    path('alojamiento/<int:alojamiento_id>/', views.alojamiento_detalle, name='alojamiento_detalle'),
]
