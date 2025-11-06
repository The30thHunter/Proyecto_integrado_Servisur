from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Cliente, Pedido, Marca, Modelo, Dispositivo,
    TipoFalla, Reparacion
)
from .formulario import LoginForm, ClienteForm, DispositivoForm, PedidoForm

# 🏠 Vista principal del panel
@login_required
def main_view(request):
    opening_hour = "09:00"
    closing_hour = "19:30"
    hoy = timezone.localtime(timezone.now()).date()
    fecha_formateada = hoy.strftime("%d/%m/%Y")

    nombre_usuario = request.user.get_full_name() or request.user.username

    context = {
        "fecha_hoy": fecha_formateada,
        "horario_apertura": opening_hour,
        "horario_cierre": closing_hour,
        "usuario_activo": nombre_usuario,
    }
    return render(request, "base_datos/main.html", context)

# 🛠️ Vista para registrar una reparación
def registrar_reparacion_view(request):
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST, prefix="cliente")
        dispositivo_form = DispositivoForm(request.POST, prefix="dispositivo")
        pedido_form = PedidoForm(request.POST, prefix="pedido")

        nuevo_modelo_nombre = request.POST.get("nuevo_modelo", "").strip()
        modelo_seleccionado = request.POST.get("dispositivo-modelo")

        if cliente_form.is_valid() and dispositivo_form.is_valid() and pedido_form.is_valid():
            try:
                with transaction.atomic():
                    cliente = cliente_form.save()
                    dispositivo = dispositivo_form.save(commit=False)
                    dispositivo.Activo = True

                    if modelo_seleccionado == "agregar_nuevo" and nuevo_modelo_nombre:
                        marca = dispositivo_form.cleaned_data.get("Marca")
                        modelo_existente = Modelo.objects.filter(Modelo__iexact=nuevo_modelo_nombre, Marca=marca).first()

                        if modelo_existente:
                            dispositivo.modelo = modelo_existente
                        else:
                            nueva_instancia = Modelo.objects.create(
                                Modelo=nuevo_modelo_nombre,
                                Marca=marca
                            )
                            dispositivo.modelo = nueva_instancia
                    else:
                        try:
                            dispositivo.modelo_id = int(modelo_seleccionado)
                        except (TypeError, ValueError):
                            messages.error(request, "Modelo seleccionado no válido.")
                            raise Exception("Modelo inválido")

                    dispositivo.save()

                    pedido = pedido_form.save(commit=False)
                    pedido.Cliente = cliente
                    pedido.Dispositivo = dispositivo

                    if not pedido.Fecha:
                        pedido.Fecha = timezone.localtime(timezone.now()).strftime("%d/%m/%Y")
                    pedido.save()

                messages.success(request, f"Reparación registrada correctamente (Orden: {pedido.N_Orden})")
                return redirect('registrar_reparacion')
            except Exception as e:
                messages.error(request, f"Ocurrió un error al guardar: {str(e)}")
        else:
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
    return render(request, "base_datos/registrar_reparacion.html", context)

# 📊 Vista para consultar estado de reparación
def estado_reparacion_view(request):
    return render(request, 'base_datos/Estado_reparacion.html')

# 📄 Vista para generar documento
def generar_documento_view(request):
    return render(request, 'base_datos/Generar_documento.html')

# 📊 Vista para generar Excel
def generar_excel_view(request):
    return render(request, 'base_datos/Generar_Excel.html')

# 🔐 Cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('main')

# 🔐 Login con mensajes personalizados
def login_view(request):
    form = LoginForm(request.POST or None)
    error_message = ''

    if request.method == 'POST' and form.is_valid():
        usuario = form.cleaned_data['username']
        clave = form.cleaned_data['password']
        user = authenticate(request, username=usuario, password=clave)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            error_message = 'El usuario no existe.' if not User.objects.filter(username=usuario).exists() else 'Contraseña incorrecta.'

    return render(request, 'login.html', {'form': form, 'error_message': error_message})

# 📋 Historial de reparaciones
def consultar_historial(request):
    rut = request.GET.get('rut')
    orden = request.GET.get('orden')
    fecha = request.GET.get('fecha')

    reparaciones = Reparacion.objects.all()

    if rut:
        reparaciones = reparaciones.filter(rut__icontains=rut)
    if orden:
        reparaciones = reparaciones.filter(numero_orden__icontains=orden)
    if fecha:
        reparaciones = Reparacion.objects.filter(fecha_ingreso=fecha)
    else:
        reparaciones = reparaciones.order_by('-fecha_ingreso')

    return render(request, 'base_datos/Consultar_historial.html', {'reparaciones': reparaciones})

# 🔄 Obtener modelos según marca (AJAX)
def obtener_modelos_por_marca(request):
    marca_id = request.GET.get('marca_id')
    modelos = Modelo.objects.filter(Marca_id=marca_id).values('id', 'Modelo')
    return JsonResponse(list(modelos), safe=False)

# 🔄 Obtener tipos de falla (AJAX)
def obtener_tipos_falla(request):
    tipos = TipoFalla.objects.all().values('id', 'nombre')
    return JsonResponse(list(tipos), safe=False)

# ➕ Agregar nuevo modelo (AJAX)
from .models import Modelo, Marca
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
@csrf_exempt
def agregar_modelo_ajax(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        marca_id = request.POST.get("marca_id")

        if not nombre or not marca_id:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

        marca = Marca.objects.filter(id=marca_id).first()
        if not marca:
            return JsonResponse({"error": "Marca no encontrada"}, status=404)

        modelo, creado = Modelo.objects.get_or_create(Modelo=nombre, Marca=marca)
        return JsonResponse({"id": modelo.id, "nombre": modelo.Modelo})




from .models import Marca
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def agregar_marca_ajax(request):
    if request.method == "POST":
        try:
            nombre = request.POST.get("nombre", "").strip()
            print("📥 Nombre recibido:", nombre)

            if not nombre:
                return JsonResponse({"error": "Nombre vacío"}, status=400)

            marca, creada = Marca.objects.get_or_create(Marca=nombre)
            print("✅ Marca creada:", marca.id, marca.Marca)

            return JsonResponse({"id": marca.id, "nombre": marca.Marca})
        except Exception as e:
            print("❌ Error interno en agregar_marca_ajax:", str(e))
            return JsonResponse({"error": "Error interno del servidor"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

