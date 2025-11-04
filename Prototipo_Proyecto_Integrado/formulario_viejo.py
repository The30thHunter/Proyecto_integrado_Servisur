from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Cliente, Pedido, Marca, Modelo, Dispositivo

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['Nombre', 'Apellido', 'Numero_telefono', 'Direccion', 'Rut']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'Apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'Numero_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'Direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'Rut': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'RUT'}),
        }
        labels = {
            'Numero_telefono': _('Número'),
            'Rut': _('RUT'),
        }

    def clean_Rut(self):
        rut = self.cleaned_data.get('Rut')
        if rut and Cliente.objects.filter(Rut=rut).exists():
            raise forms.ValidationError("Ya existe un cliente con este RUT.")
        return rut


class PedidoForm(forms.ModelForm):
    Cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(Activo=True),
        empty_label='Seleccione Cliente',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    Dispositivo = forms.ModelChoiceField(
        queryset=Dispositivo.objects.filter(Activo=True),
        empty_label='Seleccione Dispositivo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Pedido
        fields = ['Fecha', 'Coste', 'Abono', 'Restante', 'Cliente', 'Dispositivo']
        widgets = {
            'Fecha': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dd/mm/YYYY'}),
            'Coste': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Costo total'}),
            'Abono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Abono'}),
            'Restante': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Restante'}),
        }


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['Marca']
        widgets = {
            'Marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'}),
        }

    def clean_Marca(self):
        nombre = self.cleaned_data.get('Marca', '').strip()
        if nombre and Marca.objects.filter(Marca__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe una marca con ese nombre.")
        return nombre


class ModeloForm(forms.ModelForm):
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

    def clean_Modelo(self):
        nombre = self.cleaned_data.get('Modelo', '').strip()
        if nombre and Modelo.objects.filter(Modelo__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe un modelo con ese nombre.")
        return nombre


class DispositivoForm(forms.ModelForm):
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


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    password = forms.CharField(label='Contraseña',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
