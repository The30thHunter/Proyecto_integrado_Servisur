from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .formulario import LoginForm
from .models import Reparacion
from django.utils import timezone
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages

# importa tus formularios
from .formulario import ClienteForm, DispositivoForm, PedidoForm

@login_required
def main_view(request):
    # Horario configurable: cámbialo aquí si quieres
    opening_hour = "09:00"
    closing_hour = "19:30"

    # Fecha local (formato legible)
    hoy = timezone.localtime(timezone.now()).date()
    fecha_formateada = hoy.strftime("%d/%m/%Y")  # ejemplo: 04/11/2025

    # Nombre de usuario (si no autenticado mostramos 'Invitado')
    if request.user.is_authenticated:
        nombre_usuario = request.user.get_full_name() or request.user.username
    else:
        nombre_usuario = "Invitado"

    context = {
        "fecha_hoy": fecha_formateada,
        "horario_apertura": opening_hour,
        "horario_cierre": closing_hour,
        "usuario_activo": nombre_usuario,
    }
    return render(request, "base_datos/main.html", context)


def registrar_reparacion_view(request):
    """
    Vista única que muestra los formularios de Cliente, Dispositivo y Pedido
    y guarda los 3 registros en una transacción al enviar.
    """
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST, prefix="cliente")
        dispositivo_form = DispositivoForm(request.POST, prefix="dispositivo")
        pedido_form = PedidoForm(request.POST, prefix="pedido")

        # validación conjunta
        if cliente_form.is_valid() and dispositivo_form.is_valid() and pedido_form.is_valid():
            try:
                with transaction.atomic():
                    # Guardar cliente
                    cliente = cliente_form.save()

                    # Guardar dispositivo (setea Activo=True por defecto)
                    dispositivo = dispositivo_form.save(commit=False)
                    dispositivo.Activo = True
                    dispositivo.save()

                    # Guardar pedido vinculando cliente y dispositivo
                    pedido = pedido_form.save(commit=False)
                    pedido.Cliente = cliente
                    pedido.Dispositivo = dispositivo

                    # si no enviaste Fecha en el formulario, puedes asignar hoy como fallback
                    if not pedido.Fecha:
                        from django.utils import timezone
                        pedido.Fecha = timezone.localtime(timezone.now()).strftime("%d/%m/%Y")
                    pedido.save()

                messages.success(request, "Reparación registrada correctamente (Orden: {})".format(pedido.N_Orden))
                return redirect('registrar_reparacion')
            except Exception as e:
                messages.error(request, "Ocurrió un error al guardar: {}".format(str(e)))
        else:
            # si no son válidos, se muestran errores en la plantilla
            messages.error(request, "Corrige los errores del formulario.")
    else:
        cliente_form = ClienteForm(prefix="cliente")
        dispositivo_form = DispositivoForm(prefix="dispositivo")
        pedido_form = PedidoForm(prefix="pedido")

    context = {
        "cliente_form": cliente_form,
        "dispositivo_form": dispositivo_form,
        "pedido_form": pedido_form,
    }
    return render(request, "base_datos/Registrar_reparacion.html", context)


def estado_reparacion_view(request):
    return render(request, 'base_datos/Estado_reparacion.html')

def generar_documento_view(request):
    return render(request, 'base_datos/Generar_documento.html')

def generar_excel_view(request):
    return render(request, 'base_datos/Generar_Excel.html')


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