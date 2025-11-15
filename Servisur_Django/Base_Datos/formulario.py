from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Cliente, Pedido, Marca, Modelo, Dispositivo, Tipo_Falla

# 🧍 Formulario para registrar un cliente nuevo
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['Nombre', 'Apellido', 'Numero_telefono', 'Rut']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'Numero_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'Rut': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_Rut(self):
        rut = (self.cleaned_data.get('Rut') or '').strip()
        instancia = getattr(self, 'instance', None)
        qs = Cliente.objects.filter(Rut__iexact=rut)
        if instancia and instancia.pk:
            qs = qs.exclude(pk=instancia.pk)
        if rut and qs.exists():
            raise forms.ValidationError(_("Ya existe un cliente con este RUT."))
        return rut or None


# 📋 Formulario para pedidos (órdenes)
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        # Restante es campo no editable, no debe incluirse en el form
        fields = ['Fecha', 'Coste', 'Abono', 'Dispositivo', 'Activo', 'Estado', 'Observaciones', 'Tipo_de_falla']
        widgets = {
            'Fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_pedido-Fecha'}),
            'Coste': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_pedido-Coste'}),
            'Abono': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_pedido-Abono'}),
            'Dispositivo': forms.Select(attrs={'class': 'form-select', 'id': 'id_pedido-Dispositivo'}),
            'Activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Estado': forms.Select(attrs={'class': 'form-select'}),
            'Observaciones': forms.TextInput(attrs={'class': 'form-control'}),
            'Tipo_de_falla': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_Fecha(self):
        fecha = self.cleaned_data.get('Fecha')
        hoy = timezone.localdate()
        if fecha != hoy:
            raise forms.ValidationError(_("La fecha del pedido debe ser la fecha actual."))
        return fecha

    def clean(self):
        cleaned = super().clean()
        coste = cleaned.get('Coste') or 0
        abono = cleaned.get('Abono') or 0
        if abono > coste:
            self.add_error('Abono', _("El abono no puede ser mayor que el coste total."))
        return cleaned


# 🏷️ Formulario para registrar una nueva marca
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['Marca']
        widgets = {
            'Marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'}),
        }

    def clean_Marca(self):
        nombre = (self.cleaned_data.get('Marca') or '').strip()
        instancia = getattr(self, 'instance', None)
        qs = Marca.objects.filter(Marca__iexact=nombre)
        if instancia and instancia.pk:
            qs = qs.exclude(pk=instancia.pk)
        if nombre and qs.exists():
            raise forms.ValidationError(_("Ya existe una marca con ese nombre."))
        return nombre


# 📦 Formulario para registrar un modelo de dispositivo
class ModeloForm(forms.ModelForm):
    Marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        empty_label='Seleccione Marca',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Modelo
        fields = ['Modelo', 'Marca']
        widgets = {
            'Modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del modelo'}),
        }

    def clean_Modelo(self):
        nombre = (self.cleaned_data.get('Modelo') or '').strip()
        return nombre

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('Modelo', '').strip()
        marca = cleaned_data.get('Marca')
        if nombre and marca:
            qs = Modelo.objects.filter(Modelo__iexact=nombre, Marca=marca)
            instancia = getattr(self, 'instance', None)
            if instancia and instancia.pk:
                qs = qs.exclude(pk=instancia.pk)
            if qs.exists():
                raise forms.ValidationError(_("Ya existe ese modelo para la marca seleccionada."))
        return cleaned_data


# 💻 Formulario para registrar un dispositivo específico
class DispositivoForm(forms.ModelForm):
    Marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        empty_label='Seleccione marca',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'marca-select'})
    )

    modelo = forms.ModelChoiceField(
        queryset=Modelo.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'modelo-select'})
    )

    Tipo_Falla = forms.ModelChoiceField(
        queryset=Tipo_Falla.objects.all(),
        required=False,
        label="Tipo de falla",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    Codigo_Bloqueo = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1234, patrón Z, sin bloqueo'
        })
    )

    class Meta:
        model = Dispositivo
        fields = [
            "modelo",
            "Metodo_Bloqueo",
            "Codigo_Bloqueo",
            "Tipo_Falla",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Por defecto no hay modelos
        self.fields['modelo'].queryset = Modelo.objects.none()

        # Lógica para poblar modelos según la marca enviada en POST o según la instancia
        pref = getattr(self, 'prefix', None)
        marca_field_name = 'Marca'
        modelo_field_name = 'modelo'
        if pref:
            marca_field_name = f'{pref}-Marca'
            modelo_field_name = f'{pref}-modelo'

        if marca_field_name in self.data:
            try:
                raw = self.data.get(marca_field_name)
                marca_id = int(raw) if raw not in ('', None) else None
                if marca_id:
                    self.fields['modelo'].queryset = Modelo.objects.filter(Marca_id=marca_id)
            except (ValueError, TypeError):
                self.fields['modelo'].queryset = Modelo.objects.none()
        else:
            instancia = getattr(self, 'instance', None)
            if getattr(instancia, 'pk', None) and getattr(instancia, 'modelo', None):
                marca_obj = getattr(instancia.modelo, 'Marca', None)
                if marca_obj:
                    self.fields['modelo'].queryset = Modelo.objects.filter(Marca=marca_obj)
                    try:
                        self.fields['Marca'].initial = marca_obj.id
                    except Exception:
                        pass
                    try:
                        self.fields['modelo'].initial = instancia.modelo.id
                    except Exception:
                        pass


# 🔐 Formulario de login para autenticación de usuarios
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
