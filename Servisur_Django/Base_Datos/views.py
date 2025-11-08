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
    Cliente, Pedido, Marca, Modelo, Dispositivo
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



def registrar_reparacion_view(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                # 🧍 Cliente
                cliente = Cliente.objects.create(
                    Nombre=request.POST.get("cliente-Nombre", "").strip(),
                    Apellido=request.POST.get("cliente-Apellido", "").strip(),
                    Numero_telefono=request.POST.get("cliente-Numero_telefono", "").strip(),
                    Rut=int(request.POST.get("cliente-Rut", "0")),
                    Activo=True
                )

                # 📦 Marca y Modelo
                marca_id = request.POST.get("dispositivo-Marca")
                nuevo_modelo_nombre = request.POST.get("nuevo_modelo", "").strip()
                modelo_seleccionado = request.POST.get("dispositivo-modelo")

                if marca_id == "agregar_marca":
                    nueva_marca_nombre = request.POST.get("nueva_marca", "").strip()
                    marca = Marca.objects.create(Marca=nueva_marca_nombre)
                else:
                    marca = Marca.objects.get(id=int(marca_id))

                if modelo_seleccionado == "agregar_nuevo" and nuevo_modelo_nombre:
                    modelo = Modelo.objects.create(Modelo=nuevo_modelo_nombre, Marca=marca)
                else:
                    modelo = Modelo.objects.get(id=int(modelo_seleccionado))

                # 💻 Dispositivo
                dispositivo = Dispositivo.objects.create(
                    modelo=modelo,
                    Codigo_Bloqueo=request.POST.get("dispositivo-Codigo_Bloqueo", "").strip(),
                    rut=cliente,
                    Activo=True
                )

                # 📋 Pedido
                coste = int(request.POST.get("pedido-Coste", "0"))
                abono = int(request.POST.get("pedido-Abono", "0"))
                restante = coste - abono

                fecha_str = request.POST.get("pedido-Fecha")
                fecha = timezone.datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else timezone.localdate()

                pedido = Pedido.objects.create(
                    Fecha=fecha,
                    Coste=coste,
                    Abono=abono,
                    Restante=restante,
                    Dispositivo=dispositivo,
                    Estado='REG',
                    Tipo_de_falla=request.POST.get("dispositivo-Tipo_Falla", "").strip(),
                    Activo=True
                )

                messages.success(request, f"Reparación registrada correctamente (Orden: {pedido.N_Orden})")
                return redirect("registrar_reparacion")

        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar: {str(e)}")

    context = {
        "dispositivo_form": DispositivoForm(),  # Solo se usa para cargar marcas en el template
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

    pedidos = Pedido.objects.select_related('Dispositivo__rut', 'Dispositivo__modelo__Marca')

    if rut:
        pedidos = pedidos.filter(Dispositivo__rut__Rut__icontains=rut)
    if orden:
        pedidos = pedidos.filter(N_Orden__icontains=orden)
    if fecha:
        pedidos = pedidos.filter(Fecha=fecha)
    else:
        pedidos = pedidos.order_by('-Fecha')

    # Adaptar los datos al formato que espera el template
    reparaciones = []
    for pedido in pedidos:
        cliente = pedido.Dispositivo.rut
        dispositivo = pedido.Dispositivo
        modelo = dispositivo.modelo
        marca = modelo.Marca if modelo else None

        reparaciones.append({
            'nombre': cliente.Nombre if cliente else '',
            'apellido': cliente.Apellido if cliente else '',
            'numero_orden': pedido.N_Orden,
            'fecha_ingreso': pedido.Fecha,
            'rut': cliente.Rut if cliente else '',
            'marca': marca.Marca if marca else 'Sin marca',
            'equipo': modelo.Modelo if modelo else 'Sin modelo',
            'estado': dict(Pedido.ESTADOS).get(pedido.Estado, 'Desconocido'),
        })

    return render(request, 'base_datos/Consultar_historial.html', {'reparaciones': reparaciones})


# 🔄 Obtener modelos según marca (AJAX)
def obtener_modelos_por_marca(request):
    marca_id = request.GET.get('marca_id')
    modelos = Modelo.objects.filter(Marca_id=marca_id).values('id', 'Modelo')
    return JsonResponse(list(modelos), safe=False)

# 🔄 Obtener tipos de falla (AJAX)
def obtener_tipos_falla(request):
    tipos = Pedido.objects.all().values('id', 'Tipo_de_falla')
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