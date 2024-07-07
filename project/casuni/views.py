from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import LoginForm, SolicitudAlojamiento  # Ensure you have imported your updated LoginForm
from django.contrib.auth.decorators import login_required
from .models import Alojamiento, Estudiante, Propietario, Solicitud, Reserva
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .vistas.notificaciones import send_notification
from django.http import Http404, JsonResponse


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
                    return redirect('home')  # Redirect to estudiante's profile page
                elif user.propietario.exists():
                    return redirect('home')  # Redirect to propietario's profile page
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
    if  user.estudiante.all():
        estudiante = user.estudiante.first()
        return render(request, 'estudiante_perfil.html', {'estudiante': estudiante})
    else:
        propietario = user.propietario.first()
        alojamientos = Alojamiento.objects.filter(propietario=propietario.id)
        return render(request, 'propietario_perfil.html', {'propietario': propietario, 'alojamientos': alojamientos})

@login_required
def notifications(request):
    return render(request, 'notificaciones.html')

def alojamiento_detalle(request, alojamiento_id):
    alojamiento = get_object_or_404(Alojamiento, pk=alojamiento_id)
    estudiante = None  # Inicializamos como None por defecto
    solicitud_url = None
    form = None  # También inicializamos el formulario como None

    if request.user.is_authenticated:
        # Si el usuario está autenticado, intentamos obtener el estudiante
        try:
            estudiante = Estudiante.objects.get(user=request.user)
        except Estudiante.DoesNotExist:
            estudiante = None

        if request.method == 'POST':
            # Procesamiento del formulario de solicitud si se envía
            form = SolicitudAlojamiento(request.POST)

            if form.is_valid():
                fecha_desde = form.cleaned_data['fechaDesde']
                fecha_hasta = form.cleaned_data['fechaHasta']
                mensaje = form.cleaned_data['mensaje']

                if estudiante:
                    # Verificamos si ya existe una solicitud pendiente
                    existing_solicitud = Solicitud.objects.filter(
                        estudiante=estudiante,
                        alojamiento=alojamiento,
                    ).first()

                    if existing_solicitud:
                        if existing_solicitud.estado == 'P':
                            messages.error(request, 'Ya tienes una solicitud pendiente para este alojamiento.')
                            solicitud_url = reverse('solicitud', kwargs={'solicitud_id': existing_solicitud.id})
                        else:
                            solicitud_url = reverse('solicitud', kwargs={'solicitud_id': existing_solicitud.id})
                    else:
                        # Creamos la nueva solicitud
                        solicitud = Solicitud(
                            estudiante=estudiante,
                            alojamiento=alojamiento,
                            fechaInicio=fecha_desde,
                            fechaFin=fecha_hasta,
                            texto=mensaje,
                            estado='P'  
                        )
                        solicitud.save()

                        # Mostramos el mensaje de éxito
                        messages.success(request, 'La solicitud se ha creado correctamente.')

                        # Generamos la URL para la página de detalles de la solicitud
                        solicitud_url = reverse('solicitud', kwargs={'solicitud_id': solicitud.id})

                        # Reinicializamos el formulario después de enviarlo con éxito
                        form = SolicitudAlojamiento()  # Re-inicializamos con una instancia vacía

                else:
                    messages.error(request, 'Solo los estudiantes pueden realizar solicitudes de alojamiento.')

        else:
            form = SolicitudAlojamiento()
            if estudiante:
                existing_solicitud = Solicitud.objects.filter(
                    estudiante=estudiante,
                    alojamiento=alojamiento,
                ).first()
                if existing_solicitud:
                    solicitud_url = reverse('solicitud', kwargs={'solicitud_id': existing_solicitud.id})

    # Contexto con el formulario inicial o el formulario con errores
    context = {
        'alojamiento': alojamiento,
        'form': form,
        'solicitud_url': solicitud_url,
    }

    return render(request, 'alojamiento_detalle.html', context)


@login_required
def aceptar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    solicitud.estado = 'A'
    solicitud.save()
    send_notification(solicitud.estudiante.user, "Tu solicitud ha sido aceptada", "solicitud aceptada")
    return JsonResponse({'status': 'success', 'message': 'Solicitud aceptada'})

@login_required
def rechazar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    solicitud.estado = 'rechazada'
    solicitud.save()
    send_notification(solicitud.estudiante.user, "Tu solicitud ha sido rechazada", "solicitud rechazada")
    return JsonResponse({'status': 'success', 'message': 'Solicitud rechazada'})

@login_required
def solicitud(request,solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    
    context = {
        'alojamiento': solicitud.alojamiento,
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

@login_required
def crear_reserva(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    # Obtener los datos del formulario de solicitud
    fecha_desde = solicitud.fechaInicio
    fecha_hasta = solicitud.fechaFin
    mensaje = solicitud.texto

    # Crear la reserva asociada a la solicitud y al alojamiento
    reserva = Reserva(
        estudiante=solicitud.estudiante,
        alojamiento=solicitud.alojamiento,
        fechaInicio=fecha_desde,
        fechaFin=fecha_hasta,
        estado='Activa',  # Define el estado inicial de la reserva según tus necesidades
        texto=mensaje,
    )
            
    # Guardar la reserva en la base de datos
    reserva.save()
    messages.success(request, 'La reserva se ha creado correctamente.')
    return redirect('estudiante_perfil', estudiante_id=solicitud.estudiante.id) 