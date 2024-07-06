from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import LoginForm, SolicitudAlojamiento  # Ensure you have imported your updated LoginForm
from django.contrib.auth.decorators import login_required
from .models import Alojamiento, Estudiante, Propietario, Solicitud
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
                    return redirect('estudiante_home')  # Redirect to estudiante's profile page
                elif user.propietario.exists():
                    return redirect('propietario_home')  # Redirect to propietario's profile page
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
            estudiante = Estudiante.objects.get(pk=1)  # Temporary, replace with actual logic to get current user
            fecha_desde = form.cleaned_data['fechaDesde']
            fecha_hasta = form.cleaned_data['fechaHasta']
            mensaje = form.cleaned_data['mensaje']
            
            solicitud = Solicitud(
                estudiante=estudiante,  
                alojamiento=alojamiento,
                fechaInicio=fecha_desde,
                fechaFin=fecha_hasta,
                texto=mensaje,
                estado='P'  # 'P' for Pendiente
            )
            solicitud.save()
            
            # Clear form data after successful submission
            form = SolicitudAlojamiento()  # Re-initialize with an empty instance
            
            # Show success message
            messages.success(request, 'La solicitud se ha creado correctamente.')
            
            # Generate URL for solicitud detail page
            solicitud_url = reverse('solicitud', kwargs={'alojamiento_id': alojamiento_id, 'solicitud_id': solicitud.id})
            
            # Update context with solicitud URL
            context = {
                'alojamiento': alojamiento,
                'form': form,
                'solicitud_url': solicitud_url,
            }
            
            return render(request, 'alojamiento_detalle.html', context)
    else:
        form = SolicitudAlojamiento()

    # Context with initial form or form with errors
    context = {
        'alojamiento': alojamiento,
        'form': form,
    }
    
    return render(request, 'alojamiento_detalle.html', context)

def solicitud(request,alojamiento_id,solicitud_id):
    alojamiento = get_object_or_404(Alojamiento, pk=alojamiento_id)
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    
    context = {
        'alojamiento': alojamiento,
        'solicitud': solicitud,
    }
    return render(request, 'solicitud.html', context)


def estudiante_perfil(request,estudiante_id):
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    return render(request, 'estudiante_perfil.html', {'estudiante': estudiante})

def propietario_perfil(request, propietario_id):
    propietario = get_object_or_404(Propietario, id=propietario_id)
    alojamientos = Alojamiento.objects.filter(propietario=propietario)
    return render(request, 'propietario_perfil.html', {'propietario': propietario, 'alojamientos': alojamientos})