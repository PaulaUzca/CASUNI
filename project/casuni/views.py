from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import LoginForm, SolicitudAlojamiento  # Ensure you have imported your updated LoginForm
from django.contrib.auth.decorators import login_required
from .models import Alojamiento, Estudiante, Propietario, Solicitud, Reserva, Pregunta, Respuesta, Reseña
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .vistas.notificaciones import send_notification
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
def vista_propietario_perfil(request, propietario_id):
        propietario = get_object_or_404(Propietario, pk=propietario_id)
        return render(request, 'vista_perfil_propietario.html', {'propietario': propietario})



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

                if fecha_desde >= fecha_hasta:
                    messages.error(request, 'La fecha de inicio debe ser anterior a la fecha de fin.')
                elif fecha_desde < alojamiento.fecha_inicio:
                    messages.error(request, 'La fecha de inicio debe estar después de la fecha disponible del alojamiento.')
                elif alojamiento.fecha_fin and fecha_desde > alojamiento.fecha_fin:
                    messages.error(request, 'La fecha de inicio debe estar antes de la fecha límite disponible del alojamiento.')
                elif fecha_hasta and fecha_desde >= fecha_hasta:
                    messages.error(request, 'La fecha de inicio debe ser anterior a la fecha de fin.')
                elif fecha_hasta and (alojamiento.fecha_fin and fecha_hasta > alojamiento.fecha_fin):
                    messages.error(request, 'La fecha de fin debe estar antes de la fecha límite disponible del alojamiento.')
                elif estudiante:
                    # Verificamos si ya existe una solicitud pendiente
                    existing_solicitud = Solicitud.objects.filter(
                        estudiante=estudiante,
                        alojamiento=alojamiento,
                    ).first()

                    if existing_solicitud:
                            messages.error(request, 'Ya tienes una solicitud pendiente para este alojamiento.')
                            solicitud_url = reverse('solicitud', kwargs={'solicitud_id': existing_solicitud.id})
                    else:
                        # Creamos la nueva solicitud
                        solicitud = Solicitud(
                            estudiante=estudiante,
                            alojamiento=alojamiento,
                            fechaInicio=fecha_desde,
                            fechaFin=fecha_hasta,
                            texto=mensaje
                        )
                        solicitud.save()

                        # Mostramos el mensaje de éxito
                        messages.success(request, 'La solicitud se ha creado correctamente.')
                        # Generamos la URL para la página de detalles de la solicitud
                        solicitud_url = reverse('solicitud', kwargs={'solicitud_id': solicitud.id})
                        # Reinicializamos el formulario después de enviarlo con éxito
                        form = SolicitudAlojamiento()  # Re-inicializamos con una instancia vacía
                        send_notification(solicitud.alojamiento.propietario.user, f"Te ha llegado una nueva solicitud para {solicitud.alojamiento.nombre}", "solicitud_nueva")

                else:
                    messages.error(request, 'Solo los estudiantes pueden realizar solicitudes de alojamiento.')

        else:
            form = SolicitudAlojamiento()  # Re-inicializamos con una instancia vacía
            if estudiante:
                existing_solicitud = Solicitud.objects.filter(
                    estudiante=estudiante,
                    alojamiento=alojamiento,
                ).first()
                if existing_solicitud:
                    solicitud_url = reverse('solicitud', kwargs={'solicitud_id': existing_solicitud.id})

    context = {
        'alojamiento': alojamiento,
        'form': form,
        'solicitud_url': solicitud_url,
    }
    
    return render(request, 'alojamiento_detalle.html', context)


@login_required
def aceptar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    # Obtener todas las solicitudes aceptadas para el alojamiento de esta solicitud

    if Solicitud.objects.filter(
            alojamiento=solicitud.alojamiento,
            estado='A',  # Considerar solo las reservas aceptadas
            fechaInicio__lte=solicitud.fechaFin,
            fechaFin__gte=solicitud.fechaInicio
    ).exists():
        return JsonResponse({'status': 'error', 'message': 'Ya existe una solicitud aceptada para estas fechas.'})
      
    # Cambiar el estado de la solicitud
    solicitud.estado = 'A'
    solicitud.save()
    
    # Si no hay solapamientos, aceptar la solicitud y enviar la notificación
    send_notification(solicitud.estudiante.user, f"Tu solicitud para {solicitud.alojamiento.nombre} ha sido aceptada", "solicitud_aceptada")
    return JsonResponse({'status': 'success', 'message': 'Solicitud aceptada'})

@login_required
def rechazar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    solicitud.estado = 'R'
    solicitud.save()
    send_notification(solicitud.estudiante.user, f"Tu solicitud para {solicitud.alojamiento.nombre} ha sido rechazada", "solicitud rechazada")
    return JsonResponse({'status': 'success', 'message': 'Solicitud rechazada'})

@login_required
def solicitud(request,solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    # Obtener la reserva activa del estudiante para el alojamiento de la solicitud
    reserva_activa = Reserva.objects.filter(
        estudiante=solicitud.estudiante,
        estado='Activa'
    ).first()

    context = {
        'alojamiento': solicitud.alojamiento,
        'solicitud': solicitud,
        'reserva_activa': reserva_activa,
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

    # Verificar si hay una reserva activa para el alojamiento
    reserva_activa = Reserva.objects.filter(
        alojamiento=solicitud.alojamiento,
        estado='Activa'
    ).first()

    if reserva_activa:
        messages.error(request, f'El alojamiento "{solicitud.alojamiento.nombre}" ya tiene una reserva activa.')
        return redirect('estudiante_perfil', estudiante_id=solicitud.estudiante.id)

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
    send_notification(reserva.estudiante.user, f"La reserva para {solicitud.alojamiento.nombre} ha sido exitosa", "reserva")
    send_notification(reserva.alojamiento.propietario.user, f"La reserva para {solicitud.alojamiento.nombre} ha sido exitosa", "reserva")
    return redirect('estudiante_perfil', estudiante_id=solicitud.estudiante.id) 


@login_required
@csrf_exempt
def enviar_pregunta(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        alojamiento_id = request.POST.get('alojamiento_id')

        estudiante = Estudiante.objects.get(user=request.user)
        alojamiento = get_object_or_404(Alojamiento, id=alojamiento_id)

        Pregunta.objects.create(texto=question_text, alojamiento=alojamiento, estudiante = estudiante )
        send_notification(alojamiento.propietario.user, f"Nueva pregunta en {alojamiento.nombre}", "pregunta")

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)

@login_required
@csrf_exempt
def answer_question(request):
    if request.method == 'POST':
        pregunta_id = request.POST.get('pregunta_id')
        answer_text = request.POST.get('answer_text')

        pregunta = get_object_or_404(Pregunta, id=pregunta_id)
        respuesta = Respuesta.objects.create(pregunta=pregunta, texto=answer_text)

        # Optionally, notify about the answer
        send_notification(pregunta.estudiante.user, f"Respuesta a tu pregunta en {pregunta.alojamiento.nombre}", "respuesta")

        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
@csrf_exempt
def procesar_resena(request):
    if request.method == 'POST':
        review_text = request.POST.get('review')
        rating = request.POST.get('rating')
        reserva_id = request.POST.get('reserva_id')

        # Obtén el objeto Reserva usando el ID
        reserva = Reserva.objects.get(id=reserva_id)

        # Crea la reseña asociada a la reserva
        resena = Reseña.objects.create(
            texto=review_text,
            calificacion=rating,
            reserva=reserva,  # Asigna la reserva al objeto de reseña
        )

        send_notification(reserva.alojamiento.propietario.user, f"Nueva reseña en tu alojamiento {reserva.alojamiento.nombre}", "reseña")
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)