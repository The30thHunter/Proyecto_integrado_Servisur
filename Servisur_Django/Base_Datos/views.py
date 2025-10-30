from django.shortcuts import render

# Create your views here.


def main_view(request):
    return render(request, 'base_datos/main.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('main')  # Redirige al panel principal