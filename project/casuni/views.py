from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm  # Ensure you have imported your updated LoginForm
from django.contrib.auth.decorators import login_required
from .models import Alojamiento, Estudiante, Propietario

def home(request):
    print("home")

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.estudiante.exists():
                    return redirect('estudiante_home')  
                elif user.propietario.exists():
                    return redirect('propietario_home')  
            else:
                messages.error(request, 'Credenciales inválidas. Inténtelo de nuevo.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def estudiante_home(request):
    estudiante = get_object_or_404(Estudiante, user=request.user)
    nombre_usuario = request.user.username
    return render(request, 'estudiante_home.html', {'nombre_usuario': nombre_usuario, 'estudiante_id': estudiante.id})

@login_required
def propietario_home(request):
    propietario = get_object_or_404(Propietario, user=request.user)
    nombre_usuario = request.user.username
    return render(request, 'propietario_home.html', {'nombre_usuario': nombre_usuario, 'propietario_id': propietario.id})

def alojamiento_detalle(request, alojamiento_id):
    alojamiento = get_object_or_404(Alojamiento, pk=alojamiento_id)
    return render(request, 'alojamiento_detalle.html', {'alojamiento': alojamiento})

def estudiante_perfil(request,estudiante_id):
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    return render(request, 'estudiante_perfil.html', {'estudiante': estudiante})

def propietario_perfil(request, propietario_id):
    propietario = get_object_or_404(Propietario, id=propietario_id)
    alojamientos = Alojamiento.objects.filter(propietario=propietario)
    return render(request, 'propietario_perfil.html', {'propietario': propietario, 'alojamientos': alojamientos})