from django import forms
from .models import Cliente, Pedido, Marca, Modelo, Dispositivo

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['Nombre', 'Apellido', 'Numero_telefono', 'Direccion', 'Rut']

class PedidoForm(forms.ModelForm):
    Cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(Activo=True),
        empty_label='Seleccione Cliente',
        required=False
    )
    Dispositivo = forms.ModelChoiceField(
        queryset=Dispositivo.objects.filter(Activo=True),
        empty_label='Seleccione Dispositivo',
        required=False
    )

    class Meta:
        model = Pedido
        fields = ['Fecha', 'Coste', 'Abono', 'Restante', 'Cliente', 'Dispositivo']



class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['Marca']

class ModeloForm(forms.ModelForm):
    Marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        empty_label='Seleccione Marca',
        required=False
    )

    class Meta:
        model = Modelo
        fields = ['Modelo', 'Marca']


class DispositivoForm(forms.ModelForm):
    modelo = forms.ModelChoiceField(
        queryset=Modelo.objects.all(),
        empty_label='Seleccione modelo',
        required=False
    )

    class Meta:
        model = Dispositivo
        fields = ['Nombre', 'Trabajo_realizado', 'Codigo_Bloqueo', 'modelo']
