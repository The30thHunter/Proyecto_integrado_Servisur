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
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Pedido

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
        origen = request.POST.get('Origen')
        nombre = request.POST.get('Nombre') or request.POST.get('cliente-Nombre')
        apellido = request.POST.get('Apellido') or request.POST.get('cliente-Apellido')
        telefono = request.POST.get('Numero_telefono') or request.POST.get('cliente-Numero_telefono')
        rut = request.POST.get('Rut') or request.POST.get('cliente-Rut')
        dni = request.POST.get('DocumentoExtranjero') or request.POST.get('cliente-Pasaporte')

        # Buscar cliente por RUT o DNI
        cliente = None
        if origen == 'NAC' and rut:
            cliente = Cliente.objects.filter(Rut=rut).first()
        elif origen == 'EXT' and dni:
            cliente = Cliente.objects.filter(DocumentoExtranjero=dni).first()

        # Si no existe, lo creamos
        if not cliente:
            cliente = Cliente.objects.create(
                Origen=origen,
                Nombre=nombre,
                Apellido=apellido,
                Numero_telefono=telefono,
                Rut=rut if origen == 'NAC' else None,
                DocumentoExtranjero=dni if origen == 'EXT' else None,
                Activo=True
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
        qs = qs.filter(
            models.Q(Dispositivo__rut__Rut__icontains=doc) |
            models.Q(Dispositivo__rut__DocumentoExtranjero__icontains=doc)
        )


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
# 📋 Historial de reparaciones
@login_required
def consultar_historial(request):
    rut = request.GET.get('rut', '').strip()
    nombre = request.GET.get('nombre', '').strip()
    orden = request.GET.get('orden', '').strip()
    fecha = request.GET.get('fecha', '').strip()

    qs = Pedido.objects.select_related(
        'Dispositivo__rut',
        'Dispositivo__modelo__Marca',
        'Tipo_de_falla'
    ).filter(Activo=True)

    if rut:
        qs = qs.filter(Dispositivo__rut__Rut__icontains=rut)

    if nombre:
        qs = qs.filter(
            Q(Dispositivo__rut__Nombre__icontains=nombre) |
            Q(Dispositivo__rut__Apellido__icontains=nombre)
        )

    if orden:
        if orden.isdigit():
            try:
                qs = qs.filter(N_Orden=int(orden))
            except Exception:
                qs = qs.filter(N_Orden__icontains=orden)
        else:
            qs = qs.filter(N_Orden__icontains=orden)

    if fecha:
        try:
            from datetime import datetime
            parsed = datetime.strptime(fecha, "%Y-%m-%d").date()
            qs = qs.filter(Fecha=parsed)
        except Exception:
            qs = qs.filter(Fecha__icontains=fecha)

    qs = qs.order_by('-Fecha', '-N_Orden')

    reparaciones = []
    for pedido in qs:
        dispositivo = pedido.Dispositivo
        cliente = dispositivo.rut if dispositivo else None
        modelo = dispositivo.modelo if dispositivo else None
        marca = modelo.Marca if modelo and modelo.Marca else None
        tipo_falla = pedido.Tipo_de_falla

        reparaciones.append({
            'orden_id': pedido.N_Orden,
            'numero_orden': pedido.N_Orden,
            'fecha_ingreso': pedido.Fecha,
            'rut': cliente.Rut if cliente else '',
            'nombre': cliente.Nombre if cliente else '',
            'apellido': cliente.Apellido if cliente else '',
            'telefono': cliente.Numero_telefono if cliente else '',
            'marca': marca.Marca if marca else 'Sin marca',
            'equipo': modelo.Modelo if modelo else 'Sin modelo',
            'serie': dispositivo.Codigo_Bloqueo if dispositivo else '',
            'tipo_falla': tipo_falla.Falla if tipo_falla else '',
            'estado': pedido.get_Estado_display(),
            'coste': pedido.Coste,
            'abono': pedido.Abono,
            'restante': pedido.Restante,
            'observaciones': pedido.Observaciones or '',
            'activo': pedido.Activo,
        })

    context = {
        'reparaciones': reparaciones
    }
    return render(request, 'base_datos/Consultar_historial.html', context)

# 🔄 Obtener modelos según marca (AJAX)
def obtener_modelos_por_marca(request):
    marca_id = request.GET.get('marca_id')
    modelos = Modelo.objects.filter(Marca_id=marca_id).values('id', 'Modelo')
    return JsonResponse(list(modelos), safe=False)

# 🔄 Obtener tipos de falla (AJAX)
from django.http import JsonResponse
from .models import Tipo_Falla

def obtener_tipos_falla(request):
    tipos = list(Tipo_Falla.objects.all().order_by("Falla").values("id", "Falla"))
    return JsonResponse(tipos, safe=False)


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


from django.http import JsonResponse
from .models import Tipo_Falla

@csrf_exempt
# ✅ Agregar nueva falla (AJAX)
def agregar_falla_ajax(request):
    if request.method == "POST":
        texto = request.POST.get("falla", "").strip()
        if len(texto) < 3:
            return JsonResponse({"error": "La falla debe tener al menos 3 caracteres."})

        tipo_falla, creado = Tipo_Falla.objects.get_or_create(Falla=texto)
        return JsonResponse({
            "id": tipo_falla.id,
            "nombre": tipo_falla.Falla,
            "nuevo": creado
        })

    return JsonResponse({"error": "Método no permitido."}, status=405)


@login_required
def editar_reparacion_view(request, orden_id):
    pedido = get_object_or_404(Pedido, pk=orden_id)
    dispositivo = pedido.Dispositivo
    cliente = dispositivo.rut if dispositivo and dispositivo.rut else None

    if request.method == "POST":
        cliente_form = ClienteForm(request.POST, prefix="cliente", instance=cliente)
        dispositivo_form = DispositivoForm(request.POST, prefix="dispositivo", instance=dispositivo)
        pedido_form = PedidoForm(request.POST, prefix="pedido", instance=pedido)

        observaciones = request.POST.get('pedido-Observaciones', '').strip()
        tipo_falla_text = request.POST.get('dispositivo-Tipo_Falla', '').strip() or request.POST.get('nueva_falla', '').strip()

        if cliente_form.is_valid() and dispositivo_form.is_valid() and pedido_form.is_valid():
            try:
                with transaction.atomic():
                    # guardar cliente primero
                    cliente = cliente_form.save()

                    # dispositivo (no guardar aún)
                    dispositivo = dispositivo_form.save(commit=False)
                    dispositivo.rut = cliente

                    # leer marca/modelo desde POST (prefijo 'dispositivo-')
                    marca_raw = request.POST.get('dispositivo-Marca') or request.POST.get('Marca')
                    modelo_raw = request.POST.get('dispositivo-modelo') or request.POST.get('modelo')
                    nuevo_modelo_nombre = request.POST.get('nuevo_modelo', '').strip()

                    # resolver marca
                    marca = None
                    if marca_raw == 'agregar_marca':
                        nueva_marca = request.POST.get('nueva_marca', '').strip()
                        if nueva_marca:
                            marca = Marca.objects.create(Marca=nueva_marca)
                    else:
                        try:
                            marca = Marca.objects.filter(id=int(marca_raw)).first() if marca_raw not in (None, '') else None
                        except (ValueError, TypeError):
                            marca = None

                    # resolver/crear modelo y asignarlo
                    if modelo_raw == 'agregar_nuevo' and nuevo_modelo_nombre and marca:
                        modelo_existente = Modelo.objects.filter(Modelo__iexact=nuevo_modelo_nombre, Marca=marca).first()
                        if modelo_existente:
                            dispositivo.modelo = modelo_existente
                        else:
                            dispositivo.modelo = Modelo.objects.create(Modelo=nuevo_modelo_nombre, Marca=marca)
                    elif modelo_raw:
                        try:
                            dispositivo.modelo_id = int(modelo_raw)
                        except (TypeError, ValueError):
                            pass
                    # si no viene modelo, se mantiene el actual

                    dispositivo.save()

                    # tipo de falla (aceptar texto libre)
                    if tipo_falla_text:
                        tipo_falla_obj, _ = Tipo_Falla.objects.get_or_create(Falla=tipo_falla_text)
                        pedido.Tipo_de_falla = tipo_falla_obj

                    # pedido: guardar y recalcular restante
                    pedido = pedido_form.save(commit=False)
                    pedido.Dispositivo = dispositivo
                    pedido.Observaciones = observaciones
                    pedido.Restante = (pedido.Coste or 0) - (pedido.Abono or 0)
                    pedido.save()

                messages.success(request, f"Orden {pedido.N_Orden} actualizada correctamente.")
                return redirect('consultar_historial')
            except Exception as e:
                messages.error(request, f"Ocurrió un error al actualizar: {e}")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        cliente_form = ClienteForm(prefix="cliente", instance=cliente)
        dispositivo_form = DispositivoForm(prefix="dispositivo", instance=dispositivo)
        pedido_form = PedidoForm(prefix="pedido", instance=pedido)

    context = {
        "cliente_form": cliente_form,
        "dispositivo_form": dispositivo_form,
        "pedido_form": pedido_form,
        "pedido": pedido,
    }
    return render(request, "base_datos/editar_reparacion.html", context)


from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

@login_required
def pedido_json_view(request, orden_id):
    """
    Devuelve JSON con los datos básicos de la orden, cliente y dispositivo
    para poblar el modal de edición.
    """
    pedido = get_object_or_404(Pedido.objects.select_related('Dispositivo__modelo__Marca','Tipo_de_falla','Dispositivo__rut'), pk=orden_id)
    dispositivo = pedido.Dispositivo
    cliente = dispositivo.rut if dispositivo else None
    modelo_id = dispositivo.modelo.id if dispositivo and dispositivo.modelo else None
    marca_id = dispositivo.modelo.Marca.id if dispositivo and dispositivo.modelo and dispositivo.modelo.Marca else None

    # modelos disponibles para la marca (para llenar el select modelo)
    modelos = []
    if marca_id:
        modelos = list(Modelo.objects.filter(Marca_id=marca_id).values('id','Modelo'))

    data = {
        'pedido': {
            'N_Orden': pedido.N_Orden,
            'Fecha': pedido.Fecha.isoformat() if pedido.Fecha else None,
            'Coste': pedido.Coste,
            'Abono': pedido.Abono,
            'Restante': pedido.Restante,
            'Observaciones': pedido.Observaciones or '',
            'Estado': pedido.Estado,
            'Tipo_de_falla': pedido.Tipo_de_falla.Falla if pedido.Tipo_de_falla else ''
        },
        'cliente': {
            'id': cliente.id if cliente else None,
            'Nombre': cliente.Nombre if cliente else '',
            'Apellido': cliente.Apellido if cliente else '',
            'Rut': cliente.Rut if cliente else '',
            'Numero_telefono': cliente.Numero_telefono if cliente else ''
        },
        'dispositivo': {
            'id': dispositivo.id if dispositivo else None,
            'Marca_id': marca_id,
            'Modelo_id': modelo_id,
            'Codigo_Bloqueo': dispositivo.Codigo_Bloqueo if dispositivo else '',
            'Metodo_Bloqueo': dispositivo.Metodo_Bloqueo if dispositivo else ''
        },
        'modelos_de_marca': modelos,
        # opcional: lista de marcas para poblar select de marca
        'marcas': list(Marca.objects.all().values('id','Marca')),
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def pedido_actualizar_view(request, orden_id):
    """
    Recibe POST (AJAX). Valida datos mínimos y actualiza Cliente, Dispositivo y Pedido.
    Retorna JSON con éxito/error y mensajes.
    """
    try:
        pedido = get_object_or_404(Pedido, pk=orden_id)
        dispositivo = pedido.Dispositivo
        cliente = dispositivo.rut if dispositivo else None

        # leer datos enviados (esperamos application/x-www-form-urlencoded)
        nombre = request.POST.get('cliente-Nombre', '').strip()
        apellido = request.POST.get('cliente-Apellido', '').strip()
        rut = request.POST.get('cliente-Rut', '').strip()
        telefono = request.POST.get('cliente-Numero_telefono', '').strip()

        marca_id = request.POST.get('dispositivo-Marca') or None
        modelo_id = request.POST.get('dispositivo-modelo') or None
        codigo_bloqueo = request.POST.get('dispositivo-Codigo_Bloqueo', '').strip()
        metodo_bloqueo = request.POST.get('dispositivo-Metodo_Bloqueo', '').strip()

        tipo_falla_text = (request.POST.get('dispositivo-Tipo_Falla') or request.POST.get('nueva_falla') or '').strip()

        fecha = request.POST.get('pedido-Fecha') or None
        try:
            coste = int(request.POST.get('pedido-Coste') or 0)
        except ValueError:
            return JsonResponse({'ok': False, 'error': 'Coste inválido'}, status=400)
        try:
            abono = int(request.POST.get('pedido-Abono') or 0)
        except ValueError:
            return JsonResponse({'ok': False, 'error': 'Abono inválido'}, status=400)
        observaciones = request.POST.get('pedido-Observaciones', '').strip()

        # validaciones básicas
        if not rut:
            return JsonResponse({'ok': False, 'error': 'Rut vacío'}, status=400)
        if not nombre:
            return JsonResponse({'ok': False, 'error': 'Nombre vacío'}, status=400)

        with transaction.atomic():
            # actualizar cliente
            if cliente:
                cliente.Nombre = nombre
                cliente.Apellido = apellido
                cliente.Rut = rut
                cliente.Numero_telefono = telefono
                cliente.save()
            else:
                cliente = Cliente.objects.create(Nombre=nombre, Apellido=apellido, Rut=rut, Numero_telefono=telefono, Activo=True)

            # resolver/actualizar marca y modelo
            marca_obj = None
            modelo_obj = None
            if marca_id and marca_id not in ('', 'agregar_marca'):
                try:
                    marca_obj = Marca.objects.filter(id=int(marca_id)).first()
                except Exception:
                    marca_obj = None

            if modelo_id and modelo_id not in ('', 'agregar_nuevo'):
                try:
                    modelo_obj = Modelo.objects.filter(id=int(modelo_id)).first()
                except Exception:
                    modelo_obj = None

            # asignar al dispositivo
            if dispositivo is None:
                dispositivo = Dispositivo.objects.create(modelo=modelo_obj, rut=cliente, Codigo_Bloqueo=codigo_bloqueo, Metodo_Bloqueo=metodo_bloqueo, Activo=True)
            else:
                dispositivo.modelo = modelo_obj
                dispositivo.rut = cliente
                dispositivo.Codigo_Bloqueo = codigo_bloqueo
                dispositivo.Metodo_Bloqueo = metodo_bloqueo
                dispositivo.save()

            # tipo de falla
            if tipo_falla_text:
                tipo_obj, _ = Tipo_Falla.objects.get_or_create(Falla=tipo_falla_text)
                pedido.Tipo_de_falla = tipo_obj

            # pedido
            pedido.Fecha = fecha or pedido.Fecha
            pedido.Coste = coste
            pedido.Abono = abono
            pedido.Restante = coste - abono
            pedido.Observaciones = observaciones
            pedido.Dispositivo = dispositivo
            pedido.save()

        return JsonResponse({'ok': True, 'message': 'Orden actualizada'})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)

