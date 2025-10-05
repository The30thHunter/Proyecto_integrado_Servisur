from django.shortcuts import render, redirect, get_object_or_404
from .formularios import ClienteForm, PedidoForm, MarcaForm, ModeloForm, DispositivoForm
from .models import Cliente, Marca, Modelo, Pedido, Dispositivo

def crear_registro(request):
    paso = request.GET.get('paso', 'cliente')
    contexto = {}

    if paso == 'cliente':
        form = ClienteForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/agregar?paso=marca')
        contexto = {
            'form': form,
            'titulo': 'Registrar Cliente',
            'puede_omitir': Cliente.objects.exists(),
            'siguiente_paso': 'marca'
        }

    elif paso == 'marca':
        form = MarcaForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/agregar?paso=modelo')
        contexto = {
            'form': form,
            'titulo': 'Registrar Marca',
            'puede_omitir': Marca.objects.exists(),
            'siguiente_paso': 'modelo'
        }

    elif paso == 'modelo':
        form = ModeloForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/agregar?paso=dispositivo')
        contexto = {
            'form': form,
            'titulo': 'Registrar Modelo',
            'puede_omitir': Modelo.objects.exists(),
            'siguiente_paso': 'dispositivo'
        }

    elif paso == 'dispositivo':
        form = DispositivoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/agregar?paso=pedido')
        contexto = {
            'form': form,
            'titulo': 'Registrar Dispositivo'
        }

    elif paso == 'pedido':
        form = PedidoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/agregar?paso=finalizado')
        contexto = {
            'form': form,
            'titulo': 'Registrar Pedido'
        }

    elif paso == 'finalizado':
        return render(request, 'hub')

    return render(request, 'crear_registro.html', contexto)

def ver_pedidos(request):
    pedidos = Pedido.objects.select_related('Cliente', 'Dispositivo').all().order_by('-Fecha')
    return render(request, 'ver_pedidos.html', {'pedidos': pedidos})

def editar_pedido(request, n_orden):
    pedido = get_object_or_404(Pedido, N_Orden=n_orden)
    form = PedidoForm(request.POST or None, instance=pedido)

    if form.is_valid():
        form.save()
        return redirect('ver_pedidos')

    return render(request, 'editar_pedido.html', {'form': form, 'pedido': pedido})

def eliminar_pedido(request, n_orden):
    pedido = get_object_or_404(Pedido, N_Orden=n_orden)

    if request.method == 'POST':
        pedido.delete()
        return redirect('ver_pedidos')

    return render(request, 'eliminar_pedido.html', {'pedido': pedido})

def registrar_otros(request):
    return render(request,'registrar_otros.html')
    
def ver_otros(request):
    return render(request,'ver_otros.html')

def registrar_cliente(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('hub')
    return render(request, 'formulario_individual.html', {'form': form, 'titulo': 'Registrar Cliente'})

def registrar_dispositivo(request):
    form = DispositivoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('hub')
    return render(request, 'formulario_individual.html', {'form': form, 'titulo': 'Registrar Dispositivo'})

def registrar_modelo(request):
    form = ModeloForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('hub')
    return render(request, 'formulario_individual.html', {'form': form, 'titulo': 'Registrar Modelo'})

def registrar_marca(request):
    form = MarcaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('hub')
    return render(request, 'formulario_individual.html', {'form': form, 'titulo': 'Registrar Marca'})

def ver_clientes(request):
    clientes = Cliente.objects.filter(Activo=True)
    return render(request, 'ver_clientes.html', {'clientes': clientes})

def ver_dispositivos(request):
    dispositivos = Dispositivo.objects.filter(Activo=True)
    return render(request, 'ver_dispositivos.html', {'dispositivos': dispositivos})

def ver_modelos(request):
    modelos = Modelo.objects.select_related('Marca').all()
    return render(request, 'ver_modelos.html', {'modelos': modelos})

def ver_marcas(request):
    marcas = Marca.objects.all()
    return render(request, 'ver_marcas.html', {'marcas': marcas})

# Editar
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect('ver_clientes')
    return render(request, 'formulario_individual.html', {'form': form, 'titulo': 'Editar Cliente'})

def editar_dispositivo(request, pk):
    dispositivo = get_object_or_404(Dispositivo, pk=pk)
    form = DispositivoForm(request.POST or None, instance=dispositivo)
    if form.is_valid():
        form.save()
        return redirect('ver_dispositivos')
    return render(request, 'formulario_individual.html', {'form': form, 'titulo': 'Editar Dispositivo'})

def editar_modelo(request, pk):
    modelo = get_object_or_404(Modelo, pk=pk)
    form = ModeloForm(request.POST or None, instance=modelo)
    if form.is_valid():
        form.save()
        return redirect('ver_modelos')
    return render(request, 'formulario_individual.html', {'form': form, 'titulo': 'Editar Modelo'})

def editar_marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    form = MarcaForm(request.POST or None, instance=marca)
    if form.is_valid():
        form.save()
        return redirect('ver_marcas')
    return render(request, 'formulario_individual.html', {'form': form, 'titulo': 'Editar Marca'})

# Eliminar
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.Activo = False
        cliente.save()
        return redirect('ver_clientes')
    return render(request, 'eliminar_confirmacion.html', {
        'objeto': cliente,
        'tipo': 'Cliente',
        'volver': 'ver_clientes'
    })


def eliminar_dispositivo(request, pk):
    dispositivo = get_object_or_404(Dispositivo, pk=pk)
    if request.method == 'POST':
        dispositivo.Activo = False
        dispositivo.save()
        return redirect('ver_dispositivos')
    return render(request, 'eliminar_confirmacion.html', {'objeto': dispositivo, 'tipo': 'Dispositivo', 'volver': 'ver_dispositivos'})

def eliminar_modelo(request, pk):
    modelo = get_object_or_404(Modelo, pk=pk)
    if request.method == 'POST':
        modelo.delete()
        return redirect('ver_modelos')
    return render(request, 'eliminar_confirmacion.html', {'objeto': modelo, 'tipo': 'Modelo', 'volver': 'ver_modelos'})

def eliminar_marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        marca.delete()
        return redirect('ver_marcas')
    return render(request, 'eliminar_confirmacion.html', {'objeto': marca, 'tipo': 'Marca', 'volver': 'ver_marcas'})


        


def funciona(request):
    return render(request,'funciona.html')