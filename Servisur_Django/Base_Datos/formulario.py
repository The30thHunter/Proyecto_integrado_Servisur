from django import forms
from .models import Cliente, Pedido, Marca, Modelo, Dispositivo

# Formulario de Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['Nombre', 'Apellido', 'Numero_telefono', 'Direccion', 'Rut']

    def clean_Rut(self):
        rut = self.cleaned_data['Rut']
        if Cliente.objects.filter(Rut=rut).exists():
            raise forms.ValidationError("Ya existe un cliente con este RUT.")
        return rut

# Formulario de Pedido
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

# Formulario de Marca
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = '__all__'

    def clean_Marca(self):
        nombre = self.cleaned_data['Marca'].strip().lower()
        if Marca.objects.filter(Marca__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe una marca con ese nombre.")
        return self.cleaned_data['Marca']

# Formulario de Modelo
class ModeloForm(forms.ModelForm):
    Marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        empty_label='Seleccione Marca',
        required=False
    )

    class Meta:
        model = Modelo
        fields = ['Modelo', 'Marca']
    
    def clean_Modelo(self):
        nombre = self.cleaned_data['Modelo'].strip().lower()
        if Modelo.objects.filter(Modelo__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe un modelo con ese nombre.")
        return self.cleaned_data['Modelo']

# Formulario de Dispositivo
class DispositivoForm(forms.ModelForm):
    modelo = forms.ModelChoiceField(
        queryset=Modelo.objects.all(),
        empty_label='Seleccione modelo',
        required=False
    )

    class Meta:
        model = Dispositivo
        fields = ['Nombre', 'Trabajo_realizado', 'Codigo_Bloqueo', 'modelo']


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


