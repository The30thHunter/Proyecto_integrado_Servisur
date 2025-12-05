from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction, models
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.utils.dateparse import parse_date
import io
import pandas as pd
from datetime import datetime

from .decoradores import solo_administrador, solo_operador, solo_reparador
from .models import (
    Cliente, Pedido, Marca, Modelo, Dispositivo, Tipo_Falla
)
from .formulario import LoginForm, ClienteForm, DispositivoForm, PedidoForm


# 🏠 Vista principal del panel (requiere login)
from django.shortcuts import render, redirect
from django.utils import timezone

def main_view(request):
    if not request.user.is_authenticated:
        return redirect('login')   # debe existir url name='login'

    opening_hour = "09:00"
    closing_hour = "19:30"
    hoy = timezone.localtime(timezone.now()).date()
    fecha_formateada = hoy.strftime("%d/%m/%Y")

    usuario_activo = request.user.get_full_name() or request.user.username
    grupo_actual = (
        "Administrador" if (request.user.is_superuser or request.user.groups.filter(name='Administrador').exists())
        else (request.user.groups.first().name if request.user.groups.exists() else "Sin grupo")
    )

    context = {
        "fecha_hoy": fecha_formateada,
        "horario_apertura": opening_hour,
        "horario_cierre": closing_hour,
        "usuario_activo": usuario_activo,
        "grupo_actual": grupo_actual,
    }
    return render(request, "base_datos/main.html", context)




# Helpers de parsing seguro
def parse_int_safe(value, default=0):
    try:
        v = (value or "").strip()
        return int(v) if v != "" else default
    except (ValueError, TypeError):
        return default

def parse_id_safe(value):
    try:
        v = (value or "").strip()
        return int(v) if v.isdigit() else None
    except Exception:
        return None
    
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')



# 📝 Registro de reparaciones (Operador Técnico y Administrador)
@solo_operador
def registrar_reparacion(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # 🧍 Cliente
                origen = request.POST.get('Origen')
                nombre = request.POST.get('Nombre') or request.POST.get('cliente-Nombre') or ''
                apellido = request.POST.get('Apellido') or request.POST.get('cliente-Apellido') or ''
                telefono = request.POST.get('Numero_telefono') or request.POST.get('cliente-Numero_telefono') or ''
                rut = request.POST.get('Rut') or request.POST.get('cliente-Rut') or ''
                dni = request.POST.get('DocumentoExtranjero') or request.POST.get('cliente-Pasaporte') or ''

                cliente = None
                if origen == 'NAC' and rut:
                    cliente = Cliente.objects.filter(Rut=rut).first()
                elif origen == 'EXT' and dni:
                    cliente = Cliente.objects.filter(DocumentoExtranjero=dni).first()

                if not cliente:
                    cliente = Cliente.objects.create(
                        Origen=origen or 'NAC',
                        Nombre=nombre,
                        Apellido=apellido,
                        Numero_telefono=telefono,
                        Rut=rut if (origen == 'NAC') else None,
                        DocumentoExtranjero=dni if (origen == 'EXT') else None,
                        Activo=True
                    )

                # 🏷️ Marca y Modelo
                marca_id_raw = request.POST.get('dispositivo-Marca')
                nueva_marca = (request.POST.get('nueva_marca') or '').strip()
                nuevo_modelo = (request.POST.get('nuevo_modelo') or '').strip()

                if marca_id_raw == 'agregar_marca' and nueva_marca:
                    marca = Marca.objects.create(Marca=nueva_marca)
                else:
                    marca_id = parse_id_safe(marca_id_raw)
                    marca = Marca.objects.filter(id=marca_id).first() if marca_id else None

                modelo = None
                if nuevo_modelo and marca:
                    modelo, _ = Modelo.objects.get_or_create(Modelo=nuevo_modelo, Marca=marca)
                else:
                    modelo_id = parse_id_safe(request.POST.get('dispositivo-modelo'))
                    modelo = Modelo.objects.filter(id=modelo_id).first() if modelo_id else None

                # 💻 Dispositivo
                codigo_bloqueo = (request.POST.get('dispositivo-Codigo_Bloqueo') or '').strip()
                metodo_bloqueo = (request.POST.get('dispositivo-Metodo_Bloqueo') or '').strip() or 'PASS'
                dispositivo = Dispositivo.objects.create(
                    modelo=modelo,
                    rut=cliente,
                    Codigo_Bloqueo=codigo_bloqueo,
                    Metodo_Bloqueo=metodo_bloqueo,
                    Activo=True
                )

                # ⚠️ Tipo de falla
                falla_texto = (request.POST.get('dispositivo-Tipo_Falla') or '').strip()
                tipo_falla = None
                if falla_texto:
                    tipo_falla, _ = Tipo_Falla.objects.get_or_create(Falla=falla_texto)

                # 📋 Pedido (usar fecha local del servidor)
                coste = parse_int_safe(request.POST.get('pedido-Coste'), default=0)
                abono = parse_int_safe(request.POST.get('pedido-Abono'), default=0)
                restante = max(0, coste - abono)
                observaciones = (request.POST.get('pedido-Observaciones') or '').strip()

                Pedido.objects.create(
                    Fecha=timezone.localdate(),  # evita desfases por TZ
                    Coste=coste,
                    Abono=abono,
                    Restante=restante,
                    Dispositivo=dispositivo,
                    Estado='REG',
                    Tipo_de_falla=tipo_falla,
                    Observaciones=observaciones,
                    Activo=True
                )

            messages.success(request, "Reparación registrada correctamente.")
            return redirect('registrar_reparacion')

        except Exception as e:
            messages.error(request, f"Ocurrió un error al registrar: {e}")

    # GET: preparar marcas para el formulario
    marcas = Marca.objects.all()
    return render(request, 'base_datos/registrar_reparacion.html', {
        'dispositivo_form': {'fields': {'Marca': {'queryset': marcas}}},
    })


# Gestionar reparaciones (Estado y visualización)
@require_http_methods(["GET", "POST"])
@login_required
def estado_reparacion_view(request):
    u = request.user

    # Bloqueo de permisos
    if u.groups.filter(name='Operador Técnico').exists() and not (u.is_superuser or u.groups.filter(name='Administrador').exists()):
        messages.error(request, "No tienes permisos para gestionar reparaciones.")
        return redirect('main')

    if not (u.is_superuser or u.groups.filter(name__in=['Administrador', 'Técnico de Taller']).exists()):
        messages.error(request, "No tienes permisos suficientes para acceder aquí.")
        return redirect('main')

    if request.method == "POST":
        orden_id = request.POST.get("orden_id")
        nuevo_estado = request.POST.get("nuevo_estado")
        if not orden_id or not nuevo_estado:
            messages.error(request, "Datos incompletos para actualización.")
            return redirect('estado_reparacion')

        # Validar estado permitido
        valid_choices = [c[0] for c in Pedido.ESTADOS]
        if nuevo_estado not in valid_choices:
            messages.error(request, "Estado inválido.")
            return redirect('estado_reparacion')

        # Técnico de Taller: solo actualizar estado
        if u.groups.filter(name='Técnico de Taller').exists() and not (u.is_superuser or u.groups.filter(name='Administrador').exists()):
            Pedido.objects.filter(pk=orden_id).update(Estado=nuevo_estado)  # ✅ sin full_clean()
            messages.success(request, f"Orden {orden_id} actualizada a {nuevo_estado}.")
            return redirect('estado_reparacion')

        # Administrador / superuser: también usar update para evitar validaciones de fecha
        Pedido.objects.filter(pk=orden_id).update(Estado=nuevo_estado)  # ✅ sin full_clean()
        messages.success(request, f"Estado de orden {orden_id} actualizado.")
        return redirect('estado_reparacion')

    # GET: filtros (sin cambios)
    qs = Pedido.objects.select_related('Dispositivo__rut', 'Dispositivo__modelo__Marca').filter(Activo=True)

    orden = request.GET.get('orden', '').strip()
    fecha = request.GET.get('fecha', '').strip()
    doc = request.GET.get('doc', '').strip()
    nombre = request.GET.get('nombre', '').strip()
    estado = request.GET.get('estado', '').strip()

    if orden:
        qs = qs.filter(N_Orden=int(orden)) if orden.isdigit() else qs.filter(N_Orden__icontains=orden)

    if fecha:
        parsed = None
        try:
            parsed = datetime.strptime(fecha, "%Y-%m-%d").date()
        except Exception:
            try:
                parsed = datetime.strptime(fecha, "%d/%m/%Y").date()
            except Exception:
                parsed = None
        qs = qs.filter(Fecha=parsed) if parsed else qs.filter(Fecha__icontains=fecha)

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
@login_required
def generar_documento_view(request):
    u = request.user

    # Bloqueo de permisos (similar a estado_reparacion)
    if u.groups.filter(name='Operador Técnico').exists() and not (u.is_superuser or u.groups.filter(name='Administrador').exists()):
        messages.error(request, "No tienes permisos para generar documentos.")
        return redirect('main')

    if not (u.is_superuser or u.groups.filter(name__in=['Administrador', 'Técnico de Taller']).exists()):
        messages.error(request, "No tienes permisos suficientes para acceder aquí.")
        return redirect('main')

    # Filtros GET
    qs = Pedido.objects.select_related('Dispositivo__rut', 'Dispositivo__modelo__Marca').filter(Activo=True)

    orden = request.GET.get('orden', '').strip()
    fecha = request.GET.get('fecha', '').strip()
    doc = request.GET.get('doc', '').strip()
    nombre = request.GET.get('nombre', '').strip()
    estado = request.GET.get('estado', '').strip()

    if orden:
        qs = qs.filter(N_Orden=int(orden)) if orden.isdigit() else qs.filter(N_Orden__icontains=orden)

    if fecha:
        parsed = None
        try:
            parsed = datetime.strptime(fecha, "%Y-%m-%d").date()
        except Exception:
            try:
                parsed = datetime.strptime(fecha, "%d/%m/%Y").date()
            except Exception:
                parsed = None
        qs = qs.filter(Fecha=parsed) if parsed else qs.filter(Fecha__icontains=fecha)

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
    return render(request, 'base_datos/Generar_documento.html', context)


import win32print
import win32ui
from django.views.decorators.csrf import csrf_exempt

# Plantilla del ticket
plantilla_ticket = """
========================================
              SERVISUR
        Comprobante de Reparación
========================================

Nombre:        {nombre}
RUT:           {rut}
Teléfono:      {telefono}
Fecha:         {fecha}

----------------------------------------
Equipo
----------------------------------------
Marca:         {marca}
Modelo:        {modelo}
Tipo de falla: {falla}

----------------------------------------
Detalle de Pago
----------------------------------------
Total a pagar: ${total}
Abono:         ${abono}
Restante:      ${restante}

----------------------------------------
Observaciones:
{observaciones}

----------------------------------------
Firma Cliente: _________________________

========================================
        ¡Gracias por su preferencia!
========================================
"""

@csrf_exempt
def imprimir_ticket_view(request):
    if request.method == "POST":
        # Obtener datos del formulario
        data = request.POST
        contenido = plantilla_ticket.format(
            nombre=data.get("nombre", ""),
            rut=data.get("rut", ""),
            telefono=data.get("telefono", ""),
            fecha=data.get("fecha", datetime.date.today().strftime("%Y-%m-%d")),
            marca=data.get("marca", ""),
            modelo=data.get("modelo", ""),
            falla=data.get("falla", ""),
            total=data.get("total", "0"),
            abono=data.get("abono", "0"),
            restante=data.get("restante", "0"),
            observaciones=data.get("observaciones", "")
        )

        try:
            # Obtener impresora predeterminada
            printer_name = win32print.GetDefaultPrinter()
            hprinter = win32print.OpenPrinter(printer_name)
            job = win32print.StartDocPrinter(hprinter, 1, ("Ticket Servisur", None, "RAW"))
            win32print.StartPagePrinter(hprinter)
            win32print.WritePrinter(hprinter, contenido.encode('utf-8'))
            win32print.EndPagePrinter(hprinter)
            win32print.EndDocPrinter(hprinter)
            win32print.ClosePrinter(hprinter)

            return HttpResponse("Ticket enviado a la impresora correctamente.")
        except Exception as e:
            return HttpResponse(f"Error al imprimir: {str(e)}", status=500)

    return HttpResponse("Método no permitido", status=405)


# 📊 Generar Excel (solo Administrador)
@solo_administrador
def generar_excel_view(request):
    # Capturar parámetros del formulario
    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()
    estado = request.GET.get('estado', '').strip()  # REG / PRO / TER o vacío

    # Si no hay parámetros, mostrar el formulario
    if not fecha_inicio or not fecha_fin:
        return render(request, 'base_datos/Generar_Excel.html')

    # Parsear fechas
    ini = parse_date(fecha_inicio)
    fin = parse_date(fecha_fin)

    # Validar rango
    if not ini or not fin or ini > fin:
        messages.error(request, 'Rango de fechas inválido.')
        return render(request, 'base_datos/Generar_Excel.html')

    # Query filtrada
    qs = Pedido.objects.select_related(
        'Dispositivo__rut',
        'Dispositivo__modelo__Marca',
        'Tipo_de_falla'
    ).filter(Activo=True, Fecha__gte=ini, Fecha__lte=fin)

    if estado:
        qs = qs.filter(Estado=estado)

    # Construir DataFrame
    rows = []
    for p in qs:
        d = p.Dispositivo
        c = d.rut if d else None
        m = d.modelo if d else None
        marca = m.Marca.Marca if m and m.Marca else ''
        modelo = m.Modelo if m else ''
        rows.append({
            'N_Orden': p.N_Orden,
            'Fecha': p.Fecha.strftime('%Y-%m-%d') if p.Fecha else '',
            'Estado': p.get_Estado_display(),
            'Rut': c.Rut if c else '',
            'Nombre': c.Nombre if c else '',
            'Apellido': c.Apellido if c else '',
            'Telefono': c.Numero_telefono if c else '',
            'Marca': marca or 'Sin marca',
            'Modelo': modelo or 'Sin modelo',
            'Codigo_Bloqueo': d.Codigo_Bloqueo if d else '',
            'Tipo_de_falla': p.Tipo_de_falla.Falla if p.Tipo_de_falla else '',
            'Coste': p.Coste,
            'Abono': p.Abono,
            'Restante': p.Restante,
            'Observaciones': p.Observaciones or '',
            'Activo': p.Activo,
        })

    df = pd.DataFrame(rows)

    # Generar Excel en memoria
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Pedidos_filtrados', index=False)

    buffer.seek(0)
    filename = f"servisur_pedidos_{ini.strftime('%Y%m%d')}_{fin.strftime('%Y%m%d')}{('_'+estado if estado else '')}.xlsx"

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


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


# 📋 Historial de reparaciones (requiere login)
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
def obtener_tipos_falla(request):
    tipos = list(Tipo_Falla.objects.all().order_by("Falla").values("id", "Falla"))
    return JsonResponse(tipos, safe=False)


# ➕ Agregar nuevo modelo (AJAX)
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

    return JsonResponse({"error": "Método no permitido"}, status=405)


# ➕ Agregar nueva marca (AJAX)
@csrf_exempt
def agregar_marca_ajax(request):
    if request.method == "POST":
        try:
            nombre = request.POST.get("nombre", "").strip()
            if not nombre:
                return JsonResponse({"error": "Nombre vacío"}, status=400)

            marca, creada = Marca.objects.get_or_create(Marca=nombre)
            return JsonResponse({"id": marca.id, "nombre": marca.Marca})
        except Exception:
            return JsonResponse({"error": "Error interno del servidor"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


# ✅ Agregar nueva falla (AJAX)
@csrf_exempt
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


from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django import forms
from .models import Cliente, Dispositivo, Pedido, Marca, Modelo, Tipo_Falla

# -------------------------
# ModelForms (ajusta si quieres campos distintos)
# -------------------------
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['Nombre', 'Apellido', 'Rut', 'Numero_telefono']


class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        # 'modelo' es FK a Modelo; 'rut' es FK a Cliente
        fields = ['modelo', 'Metodo_Bloqueo', 'Codigo_Bloqueo', 'rut']


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['Fecha', 'Coste', 'Abono', 'Estado', 'Observaciones', 'Tipo_de_falla']


# -------------------------
# Vista: editar_reparacion_view
# -------------------------
@require_http_methods(["GET", "POST"])
def editar_reparacion_view(request, orden_id):
    """
    GET:
      - Si es petición normal, renderiza una página con los forms (opcional).
      - Si tu frontend usa otro endpoint para JSON (p.ej. /reparacion/<id>/json/), puedes omitir la rama GET.
    POST:
      - Valida los tres forms con prefijos: 'cliente', 'dispositivo', 'pedido'.
      - Si todos son válidos guarda dentro de una transacción.
      - Si la petición es AJAX devuelve JsonResponse {'ok': True} o {'ok': False, 'errores': {...}}.
      - Si no es AJAX redirige o renderiza con errores.
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    # Cargar pedido con select_related para evitar consultas adicionales
    ped = get_object_or_404(Pedido.objects.select_related('Dispositivo__rut', 'Dispositivo__modelo__Marca', 'Tipo_de_falla'), pk=orden_id)
    disp = ped.Dispositivo  # nota: en tu modelo el campo se llama Dispositivo (mayúscula)
    cli = disp.rut if disp else None

    if request.method == 'GET':
        # Si quieres devolver JSON para el modal, puedes construir y devolver los datos aquí.
        # Por simplicidad devolvemos un render con forms prellenados (opcional).
        cliente_form = ClienteForm(prefix='cliente', instance=cli)
        dispositivo_form = DispositivoForm(prefix='dispositivo', instance=disp)
        pedido_form = PedidoForm(prefix='pedido', instance=ped)
        context = {
            'cliente_form': cliente_form,
            'dispositivo_form': dispositivo_form,
            'pedido_form': pedido_form,
            'pedido': ped,
        }
        return render(request, 'consultar_reparacion.html', context)

    # POST: construir forms con prefijos (coinciden con los names del frontend)
    cliente_form = ClienteForm(request.POST, prefix='cliente', instance=cli)
    dispositivo_form = DispositivoForm(request.POST, prefix='dispositivo', instance=disp)
    pedido_form = PedidoForm(request.POST, prefix='pedido', instance=ped)

    # Validar los forms; si alguno falla, no se guarda nada
    if not (cliente_form.is_valid() and dispositivo_form.is_valid() and pedido_form.is_valid()):
        errores = {
            'cliente': {k: list(v) for k, v in cliente_form.errors.items()},
            'dispositivo': {k: list(v) for k, v in dispositivo_form.errors.items()},
            'pedido': {k: list(v) for k, v in pedido_form.errors.items()},
        }
        if is_ajax:
            return JsonResponse({'ok': False, 'errores': errores})
        # Si no es AJAX, renderiza la plantilla con los forms y errores
        context = {
            'cliente_form': cliente_form,
            'dispositivo_form': dispositivo_form,
            'pedido_form': pedido_form,
            'pedido': ped,
        }
        return render(request, 'consultar_reparacion.html', context)

    # Si llegamos aquí, todos los forms son válidos: guardar dentro de una transacción
    try:
        with transaction.atomic():
            cliente_obj = cliente_form.save()
            dispositivo_obj = dispositivo_form.save(commit=False)
            # Asegura la relación cliente <-> dispositivo
            dispositivo_obj.rut = cliente_obj
            dispositivo_obj.save()
            pedido_obj = pedido_form.save(commit=False)
            pedido_obj.Dispositivo = dispositivo_obj
            pedido_obj.save()
    except Exception as e:
        # Error inesperado al guardar: devolver como error general
        if is_ajax:
            return JsonResponse({'ok': False, 'errores': {'cliente': {}, 'dispositivo': {}, 'pedido': {'__all__': [str(e)]}}})
        # Para petición normal, mostrar mensaje y redirigir o renderizar
        context = {
            'cliente_form': cliente_form,
            'dispositivo_form': dispositivo_form,
            'pedido_form': pedido_form,
            'pedido': ped,
            'error_general': str(e),
        }
        return render(request, 'consultar_reparacion.html', context)

    # Guardado exitoso
    if is_ajax:
        return JsonResponse({'ok': True})
    # Si no es AJAX, redirige al historial con mensaje
    from django.contrib import messages
    messages.success(request, f'Orden {orden_id} actualizada correctamente.')
    return redirect('consultar_historial')




# 🔄 Datos JSON para modal de edición (requiere login)
@login_required
def pedido_json_view(request, orden_id):
    pedido = get_object_or_404(Pedido.objects.select_related('Dispositivo__modelo__Marca','Tipo_de_falla','Dispositivo__rut'), pk=orden_id)
    dispositivo = pedido.Dispositivo
    cliente = dispositivo.rut if dispositivo else None
    modelo_id = dispositivo.modelo.id if dispositivo and dispositivo.modelo else None
    marca_id = dispositivo.modelo.Marca.id if dispositivo and dispositivo.modelo and dispositivo.modelo.Marca else None

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
        'marcas': list(Marca.objects.all().values('id','Marca')),
        
        
        'fallas': list(Tipo_Falla.objects.all().values('id','Falla')),
    }
    return JsonResponse(data)


# 🔧 Actualizar estado de pedido (solo Técnico de Taller y Administrador)
@solo_reparador
@require_http_methods(["POST"])
def pedido_actualizar_view(request, orden_id):
    pedido = get_object_or_404(Pedido, pk=orden_id)
    nuevo_estado = request.POST.get("nuevo_estado", "").strip()

    valid_choices = [c[0] for c in Pedido.ESTADOS]
    if nuevo_estado not in valid_choices:
        return JsonResponse({'ok': False, 'error': 'Estado inválido'}, status=400)

    # Si es Técnico de Taller, opcionalmente permitir solo TER
    if request.user.groups.filter(name='Técnico de Taller').exists() and not (
        request.user.is_superuser or request.user.groups.filter(name='Administrador').exists()
    ):
        # Descomenta si quieres forzar solo TER:
        # if nuevo_estado != 'TER':
        #     return JsonResponse({'ok': False, 'error': "Solo puedes marcar como 'Terminado'."}, status=403)

        # ✅ Actualizar directamente sin disparar validaciones de fecha
        Pedido.objects.filter(pk=pedido.pk).update(Estado=nuevo_estado)
        return JsonResponse({'ok': True, 'message': f'Orden {pedido.N_Orden} actualizada a {nuevo_estado}.'})

    # Administrador / superuser
    Pedido.objects.filter(pk=pedido.pk).update(Estado=nuevo_estado)
    return JsonResponse({'ok': True, 'message': f'Estado de orden {pedido.N_Orden} actualizado.'})


