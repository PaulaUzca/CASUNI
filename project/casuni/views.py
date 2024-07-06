from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, SolicitudAlojamiento  # Ensure you have imported your updated LoginForm
from django.contrib.auth.decorators import login_required
from .models import Alojamiento, Estudiante, Propietario
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


def home(request):
    usuario = request.user
    alojamientos = Alojamiento.objects.all()

    return render(request, "home.html", {"usuario": usuario, "alojamientos": alojamientos})






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
def logout(request):
    auth_logout(request)
    return redirect('home')


@login_required
def perfil(request):
    user = user=request.user
    nombre_usuario = request.user.username
    if  user.estudiante:
        estudiante = get_object_or_404(Estudiante, user=request.user)
        return render(request, 'estudiante_perfil.html', {'estudiante': estudiante})
    else:
        propietario = get_object_or_404(Propietario, user)
        alojamientos = Alojamiento.objects.filter(propietario=propietario)
        return render(request, 'propietario_perfil.html', {'propietario': propietario, 'alojamientos': alojamientos})

@login_required
def notifications(request):
    return render(request, 'notificaciones.html')

def alojamiento_detalle(request, alojamiento_id):
    alojamiento = get_object_or_404(Alojamiento, pk=alojamiento_id)
    if request.method == 'POST':
        form = SolicitudAlojamiento(request.POST)
        
        if form.is_valid():
            # Process form data here
            fecha_desde = form.cleaned_data['fechaDesde']
            fecha_hasta = form.cleaned_data['fechaHasta']
            mensaje = form.cleaned_data['mensaje']
            # Additional processing or saving to database
    else:
        form = SolicitudAlojamiento()

    context = {
        'alojamiento': alojamiento,
        'form': form,
    }
    return render(request, 'alojamiento_detalle.html', context)


def estudiante_perfil(request,estudiante_id):
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    return render(request, 'estudiante_perfil.html', {'estudiante': estudiante})

def propietario_perfil(request, propietario_id):
    propietario = get_object_or_404(Propietario, id=propietario_id)
    alojamientos = Alojamiento.objects.filter(propietario=propietario)
    return render(request, 'propietario_perfil.html', {'propietario': propietario, 'alojamientos': alojamientos})