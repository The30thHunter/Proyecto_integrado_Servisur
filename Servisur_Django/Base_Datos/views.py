from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .formulario import LoginForm
from .models import Reparacion

@login_required
def main_view(request):
    return render(request, 'base_datos/main.html')

# Cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('main')

# Login con mensajes personalizados
def login_view(request):
    form = LoginForm(request.POST or None)
    error_message = ''

    if request.method == 'POST':
        if form.is_valid():
            usuario = form.cleaned_data['username']
            clave = form.cleaned_data['password']
            user = authenticate(request, username=usuario, password=clave)

            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                if not User.objects.filter(username=usuario).exists():
                    error_message = 'El usuario no existe.'
                else:
                    error_message = 'Contraseña incorrecta.'

    return render(request, 'login.html', {'form': form, 'error_message': error_message})

# Historial de reparaciones
def consultar_historial(request):
    rut = request.GET.get('rut')
    orden = request.GET.get('orden')
    fecha = request.GET.get('fecha')

    if rut or orden:
        reparaciones = Reparacion.objects.all()
        if rut:
            reparaciones = reparaciones.filter(rut__icontains=rut)
        if orden:
            reparaciones = reparaciones.filter(numero_orden__icontains=orden)
    elif fecha:
        reparaciones = Reparacion.objects.filter(fecha_ingreso=fecha)
    else:
        reparaciones = Reparacion.objects.all().order_by('-fecha_ingreso')

    return render(request, 'base_datos/Consultar_historial.html', {'reparaciones': reparaciones})

