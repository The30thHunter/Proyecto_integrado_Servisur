from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .formulario import LoginForm
from django.contrib.auth import authenticate, login


# Create your views here.

@login_required
def main_view(request):
    return render(request, 'base_datos/main.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('main') 


def login_view(request):
    form = LoginForm(request.POST or None)
    mensaje = ''

    if request.method == 'POST':
        if form.is_valid():
            usuario = form.cleaned_data['username']
            clave = form.cleaned_data['password']
            user = authenticate(request, username=usuario, password=clave)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                mensaje = 'Usuario o contraseña incorrectos'

    return render(request, 'login.html', {'form': form, 'mensaje': mensaje})
