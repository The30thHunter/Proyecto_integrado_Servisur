from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from datetime import datetime


from .models import (
    Cliente, Pedido, Marca, Modelo, Dispositivo,Tipo_Falla
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



def registrar_reparacion(request):
    if request.method == 'POST':
        # 🧍 Cliente
        nombre = request.POST.get('cliente-Nombre')
        apellido = request.POST.get('cliente-Apellido')
        telefono = request.POST.get('cliente-Numero_telefono')
        rut = request.POST.get('cliente-Rut')

        cliente, _ = Cliente.objects.get_or_create(
            Rut=rut,
            defaults={
                'Nombre': nombre,
                'Apellido': apellido,
                'Numero_telefono': telefono,
                'Activo': True,
            }
        )

        # 🏷️ Marca y Modelo
        marca_id = request.POST.get('dispositivo-Marca')
        nueva_marca = request.POST.get('nueva_marca')
        nuevo_modelo = request.POST.get('nuevo_modelo')

        if marca_id == 'agregar_marca' and nueva_marca:
            marca = Marca.objects.create(Marca=nueva_marca)
        else:
            marca = Marca.objects.filter(id=marca_id).first()

        modelo = None
        if nuevo_modelo:
            modelo, _ = Modelo.objects.get_or_create(Modelo=nuevo_modelo, Marca=marca)
        else:
            modelo_id = request.POST.get('dispositivo-modelo')
            modelo = Modelo.objects.filter(id=modelo_id).first()

        # 💻 Dispositivo
        codigo_bloqueo = request.POST.get('dispositivo-Codigo_Bloqueo')
        dispositivo = Dispositivo.objects.create(
            modelo=modelo,
            rut=cliente,
            Codigo_Bloqueo=codigo_bloqueo,
            Activo=True
        )

        # ⚠️ Tipo de falla
        falla_texto = request.POST.get('dispositivo-Tipo_Falla')
        tipo_falla, _ = Tipo_Falla.objects.get_or_create(Falla=falla_texto)

        # 📋 Pedido
        fecha = request.POST.get('pedido-Fecha')
        coste = int(request.POST.get('pedido-Coste', 0))
        abono = int(request.POST.get('pedido-Abono', 0))
        restante = coste - abono

        Pedido.objects.create(
            Fecha=fecha,
            Coste=coste,
            Abono=abono,
            Restante=restante,
            Dispositivo=dispositivo,
            Estado='REG',
            Tipo_de_falla=tipo_falla,
            Activo=True
        )

        messages.success(request, "Reparación registrada correctamente.")
        return redirect('registrar_reparacion')

    # GET: preparar marcas para el formulario
    marcas = Marca.objects.all()
    return render(request, 'base_datos/registrar_reparacion.html', {
        'dispositivo_form': {'fields': {'Marca': {'queryset': marcas}}},
    })



@login_required
@require_http_methods(["GET", "POST"])
def estado_reparacion_view(request):
    # POST: actualizar estado de una orden
    if request.method == "POST":
        orden_id = request.POST.get("orden_id")
        nuevo_estado = request.POST.get("nuevo_estado")
        if orden_id and nuevo_estado:
            pedido = get_object_or_404(Pedido, pk=orden_id)
            valid_choices = [c[0] for c in Pedido.ESTADOS]
            if nuevo_estado in valid_choices:
                pedido.Estado = nuevo_estado
                pedido.save()
                messages.success(request, f"Estado de orden {pedido.N_Orden} actualizado.")
            else:
                messages.error(request, "Estado inválido.")
        else:
            messages.error(request, "Datos incompletos para actualización.")
        return redirect('estado_reparacion')

    # GET: aplicar filtros
    qs = Pedido.objects.select_related('Dispositivo__rut', 'Dispositivo__modelo__Marca').filter(Activo=True)

    orden = request.GET.get('orden', '').strip()
    fecha = request.GET.get('fecha', '').strip()
    doc = request.GET.get('doc', '').strip()
    nombre = request.GET.get('nombre', '').strip()
    estado = request.GET.get('estado', '').strip()

    if orden:
        if orden.isdigit():
            qs = qs.filter(N_Orden=int(orden))
        else:
            qs = qs.filter(N_Orden__icontains=orden)

    if fecha:
        parsed = None
        try:
            parsed = datetime.strptime(fecha, "%Y-%m-%d").date()
        except Exception:
            try:
                parsed = datetime.strptime(fecha, "%d/%m/%Y").date()
            except Exception:
                parsed = None
        if parsed:
            qs = qs.filter(Fecha=parsed)
        else:
            qs = qs.filter(Fecha__icontains=fecha)

    if doc:
        qs = qs.filter(Dispositivo__rut__Rut__icontains=doc)

    if nombre:
        qs = qs.filter(
            models.Q(Dispositivo__rut__Nombre__icontains=nombre) |
            models.Q(Dispositivo__rut__Apellido__icontains=nombre)
        )

    if estado:
        qs = qs.filter(Estado=estado)

    qs = qs.order_by('-Fecha', '-N_Orden')[:500]

    context = {
        'pedidos': qs,
        'filtros': {'orden': orden, 'fecha': fecha, 'doc': doc, 'nombre': nombre, 'estado': estado},
        'estado_choices': Pedido.ESTADOS,
    }
    return render(request, 'base_datos/Estado_reparacion.html', context)




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