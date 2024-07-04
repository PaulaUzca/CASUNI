from django.urls import path
from . import views  # Import your views from the same app

urlpatterns = [
    path('login/', views.login_view, name='login'),      # Example path for login view
    path('', views.home, name='home'),  # Example path for dashboard view
    # Add other URLs as needed
]
