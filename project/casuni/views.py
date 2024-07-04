from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm  # Ensure you have imported your updated LoginForm

def home(request):
    print("home")

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('/')  # Update with your desired redirect URL
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
