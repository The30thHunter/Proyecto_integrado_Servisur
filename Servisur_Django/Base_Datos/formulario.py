from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Cliente, Pedido, Marca, Modelo, Dispositivo

# Formulario para registrar un cliente nuevo
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['Nombre', 'Apellido', 'Numero_telefono', 'Direccion', 'Rut']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'Numero_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'Direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'Rut': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # Validación para evitar duplicados de RUT
    def clean_Rut(self):
        rut = self.cleaned_data.get('Rut')
        if rut and Cliente.objects.filter(Rut=rut).exists():
            raise forms.ValidationError("Ya existe un cliente con este RUT.")
        return rut


# Formulario para registrar un pedido (orden de reparación)
class PedidoForm(forms.ModelForm):
    Cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(Activo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    Dispositivo = forms.ModelChoiceField(
        queryset=Dispositivo.objects.filter(Activo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Pedido
        fields = ['Fecha', 'Coste', 'Abono', 'Restante', 'Cliente', 'Dispositivo']
        widgets = {
            'Fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_pedido-Fecha'}),
            'Coste': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_pedido-Coste'}),
            'Abono': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_pedido-Abono'}),
            'Restante': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_pedido-Restante'}),
        }



# Formulario para registrar una nueva marca
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['Marca']
        widgets = {
            'Marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'}),
        }

    # Validación para evitar duplicados de marca
    def clean_Marca(self):
        nombre = self.cleaned_data.get('Marca', '').strip()
        if nombre and Marca.objects.filter(Marca__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe una marca con ese nombre.")
        return nombre


# Formulario para registrar un modelo de dispositivo
class ModeloForm(forms.ModelForm):
    # Campo para seleccionar marca
    Marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        empty_label='Seleccione Marca',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Modelo
        fields = ['Modelo', 'Marca']
        widgets = {
            'Modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del modelo'}),
        }

    # Validación para evitar duplicados de modelo
    def clean_Modelo(self):
        nombre = self.cleaned_data.get('Modelo', '').strip()
        if nombre and Modelo.objects.filter(Modelo__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe un modelo con ese nombre.")
        return nombre


# Formulario para registrar un dispositivo específico
class DispositivoForm(forms.ModelForm):
    # Campo para seleccionar modelo
    modelo = forms.ModelChoiceField(
        queryset=Modelo.objects.all(),
        empty_label='Seleccione modelo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Dispositivo
        fields = ['Nombre', 'Trabajo_realizado', 'Codigo_Bloqueo', 'modelo']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del equipo (ej. iPhone 11)'}),
            'Trabajo_realizado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Trabajo a realizar'}),
            'Codigo_Bloqueo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de bloqueo / contraseña'}),
        }


# Formulario de login para autenticación de usuarios
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
