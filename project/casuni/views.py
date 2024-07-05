from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm  # Ensure you have imported your updated LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
                    return redirect('estudiante_home')  # Redirige a la página de estudiante
                elif user.propietario.exists():
                    return redirect('propietario_home')  # Redirige a la página de propietario
                else:
                    return redirect('/') 
            else:
                messages.error(request, 'Credenciales inválidas. Inténtelo de nuevo.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def estudiante_home(request):
    return render(request, 'estudiante_home.html')

@login_required
def propietario_home(request):
    return render(request, 'propietario_home.html')

@login_required  
def estudiante_home(request):
    nombre_usuario = request.user.username
    return render(request, 'estudiante_home.html', {'nombre_usuario': nombre_usuario})

@login_required  
def propietario_home(request):
    nombre_usuario = request.user.username
    return render(request, 'propietario_home.html', {'nombre_usuario': nombre_usuario})
