from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

# 🧍 Modelo para clientes
class Cliente(models.Model):
    ORIGEN_CHOICES = [
        ('NAC', 'Nacional'),
        ('EXT', 'Extranjero'),
    ]

    Origen = models.CharField(max_length=3, choices=ORIGEN_CHOICES, default='NAC')
    Nombre = models.CharField(max_length=20)
    Apellido = models.CharField(max_length=20)
    Numero_telefono = models.CharField(max_length=15, null=True, blank=True)
    Rut = models.CharField(max_length=50, null=True, blank=True)
    DocumentoExtranjero = models.CharField(max_length=50, null=True, blank=True)
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.Nombre} {self.Apellido} ({self.Origen})"


# 🏷️ Marca de dispositivos
class Marca(models.Model):
    Marca = models.CharField(max_length=100)

    class Meta:
        constraints = [
            # Garantiza unicidad case-insensitive sobre el nombre de marca
            UniqueConstraint(Lower('Marca'), name='unique_marca_ci')
        ]

    def clean(self):
        # Normalizar espacios y validar duplicados case-insensitive
        if self.Marca:
            self.Marca = self.Marca.strip()
            if Marca.objects.exclude(pk=self.pk).filter(Marca__iexact=self.Marca).exists():
                raise ValidationError({'Marca': 'La marca ya existe.'})

    def save(self, *args, **kwargs):
        if self.Marca:
            self.Marca = self.Marca.strip()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Marca


# 📦 Modelo de dispositivos
class Modelo(models.Model):
    Modelo = models.CharField(max_length=50)
    Marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="modelos")

    class Meta:
        verbose_name_plural = "Modelos"
        constraints = [
            # Unicidad case-insensitive por par (Marca, Modelo)
            UniqueConstraint(Lower('Modelo'), 'Marca', name='unique_modelo_por_marca_ci')
        ]

    def clean(self):
        # Normalizar y validar duplicados case-insensitive por marca
        if self.Modelo:
            self.Modelo = self.Modelo.strip()
            if self.Marca and Modelo.objects.exclude(pk=self.pk).filter(Marca=self.Marca, Modelo__iexact=self.Modelo).exists():
                raise ValidationError({'Modelo': 'El modelo ya existe para esa marca.'})

    def save(self, *args, **kwargs):
        if self.Modelo:
            self.Modelo = self.Modelo.strip()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        marca = self.Marca.Marca if self.Marca else "Sin marca"
        modelo = self.Modelo if self.Modelo else "Sin modelo"
        return f"{marca} {modelo}"


# 💻 Modelo para dispositivos registrados
class Dispositivo(models.Model):
    PATRON_MATRIZ = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    METODOS_CHOICES = [
        ('PIN', 'PIN'),
        ('PASS', 'Contraseña'),
        ('PATRON', 'Patrón (matriz 3x3)'),
    ]
    modelo = models.ForeignKey(Modelo, on_delete=models.SET_NULL, null=True, related_name="dispositivos")
    Activo = models.BooleanField(default=True)
    rut = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, related_name="dispositivos")
    Metodo_Bloqueo = models.CharField(max_length=6, choices=METODOS_CHOICES, default='PASS')
    Codigo_Bloqueo = models.CharField(max_length=50, blank=True)

    def __str__(self):
        marca = self.modelo.Marca.Marca if self.modelo and self.modelo.Marca else "Sin marca"
        modelo = self.modelo.Modelo if self.modelo else "Sin modelo"
        return f"{marca} {modelo}"

    class Meta:
        verbose_name_plural = "Dispositivos"


class Tipo_Falla(models.Model):
    Falla = models.CharField(max_length=100, unique=True)

    def clean(self):
        if self.Falla:
            self.Falla = self.Falla.strip()
            if Tipo_Falla.objects.exclude(pk=self.pk).filter(Falla__iexact=self.Falla).exists():
                raise ValidationError({'Falla': 'La falla ya existe.'})

    def save(self, *args, **kwargs):
        if self.Falla:
            self.Falla = self.Falla.strip()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Falla


# 📋 Modelo para pedidos (órdenes de reparación)
class Pedido(models.Model):
    ESTADOS = [
        ('REG', 'Registrado'),
        ('PRO', 'En proceso'),
        ('TER', 'Terminado'),
    ]
    N_Orden = models.AutoField(primary_key=True)
    Fecha = models.DateField()
    Coste = models.PositiveIntegerField()
    Abono = models.PositiveIntegerField()
    Restante = models.PositiveIntegerField(editable=False)
    Dispositivo = models.ForeignKey(Dispositivo, on_delete=models.SET_NULL, null=True, related_name="pedidos")
    Activo = models.BooleanField(default=True)
    Estado = models.CharField(max_length=3, choices=ESTADOS, default='REG')
    Observaciones = models.CharField(max_length=50, null=True, blank=True)
    Tipo_de_falla = models.ForeignKey(Tipo_Falla, on_delete=models.SET_NULL, null=True, related_name="pedidos")

    class Meta:
        verbose_name_plural = "Pedidos"

    def clean(self):
        # Validaciones de integridad de negocio
        super().clean()

        # Fecha: debe ser la fecha actual (ni pasada ni futura)
        hoy = timezone.localdate()
        if self.Fecha != hoy:
            raise ValidationError({'Fecha': 'La fecha del pedido debe ser la fecha actual.'})

        # Coste y Abono ya son PositiveIntegerField, pero validar la relación
        if self.Abono > self.Coste:
            raise ValidationError({'Abono': 'El abono no puede ser mayor que el coste total.'})

    def save(self, *args, **kwargs):
        # Normalizar y calcular restante antes de guardar
        if self.Coste is None:
            self.Coste = 0
        if self.Abono is None:
            self.Abono = 0
        restante = self.Coste - self.Abono
        self.Restante = restante if restante >= 0 else 0

        # Ejecutar validaciones completas antes de persistir
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Orden #{self.N_Orden}"
