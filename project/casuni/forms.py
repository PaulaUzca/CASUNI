from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter password'
    }))

class SolicitudAlojamiento(forms.Form):
    fechaDesde = forms.DateField(label='Fecha Desde', widget=forms.DateInput(attrs={'type': 'date'}))
    fechaHasta = forms.DateField(label='Fecha Hasta', widget=forms.DateInput(attrs={'type': 'date'}))
    mensaje = forms.CharField(label='Mensaje', widget=forms.Textarea(attrs={'rows': 3}))