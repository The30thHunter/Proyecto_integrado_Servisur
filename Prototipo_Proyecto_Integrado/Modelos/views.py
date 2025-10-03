from django.shortcuts import render, redirect
from .formularios import ClienteForm, PedidoForm, MarcaForm, ModeloForm, DispositivoForm
from .models import Cliente, Marca, Modelo

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
        return render(request, 'crear_registro.html', {
            'form': None,
            'titulo': 'Registro completado',
            'mensaje': 'Todos los datos han sido registrados correctamente.'
        })

    return render(request, 'crear_registro.html', contexto)

        


def funciona(request):
    return render(request,'funciona.html')