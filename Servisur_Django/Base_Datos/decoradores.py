# Base_Datos/decoradores.py
from django.shortcuts import redirect
from django.contrib import messages

def requiere_grupo(nombre_grupo):
    def decorator(view_func):
        def _wrapped(request, *args, **kwargs):
            u = request.user
            if not u.is_authenticated:
                messages.error(request, "Debes iniciar sesión.")
                return redirect('login')
            # Admin sin restricciones
            if u.is_superuser or u.groups.filter(name='Administrador').exists():
                return view_func(request, *args, **kwargs)
            # Grupo requerido
            if u.groups.filter(name=nombre_grupo).exists():
                return view_func(request, *args, **kwargs)
            messages.error(request, "No tienes permisos suficientes para acceder aquí.")
            return redirect('main')
        return _wrapped
    return decorator

solo_administrador = requiere_grupo('Administrador')
solo_operador     = requiere_grupo('Operador Técnico')
solo_reparador    = requiere_grupo('Técnico de Taller')
