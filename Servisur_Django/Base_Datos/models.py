from django.db import models

# 🧍 Modelo para clientes
class Cliente(models.Model):
    Nombre = models.CharField(max_length=20)
    Apellido = models.CharField(max_length=20)
    Numero_telefono = models.CharField(max_length=15)
    Direccion = models.CharField(max_length=50)
    Rut = models.IntegerField()
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.Nombre} {self.Apellido}"

    class Meta:
        verbose_name_plural = "Clientes"

# 🏷️ Marca de dispositivos
class Marca(models.Model):
    Marca = models.CharField(max_length=100)

    def __str__(self):
        return self.Marca


# 📦 Modelo de dispositivos
class Modelo(models.Model):
    Modelo = models.CharField(max_length=50)
    Marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="modelos")

    def __str__(self):
        return f"{self.Marca.Marca} {self.Modelo}"

    class Meta:
        verbose_name_plural = "Modelos"

# 🧩 Tipo de falla
class TipoFalla(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tipos de falla"

# 💻 Modelo para dispositivos registrados
class Dispositivo(models.Model):
    Marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, related_name="dispositivos")
    modelo = models.ForeignKey(Modelo, on_delete=models.SET_NULL, null=True, related_name="dispositivos")
    Tipo_de_falla = models.ForeignKey(TipoFalla, on_delete=models.SET_NULL, null=True, related_name="dispositivos")
    Codigo_Bloqueo = models.CharField(max_length=50)
    Activo = models.BooleanField(default=True)

    def __str__(self):
        marca = self.Marca.Marca if self.Marca else "Sin marca"
        modelo = self.modelo.Modelo if self.modelo else "Sin modelo"
        return f"{marca} {modelo}"

    class Meta:
        verbose_name_plural = "Dispositivos"

# 📋 Modelo para pedidos (órdenes de reparación)
class Pedido(models.Model):
    N_Orden = models.AutoField(primary_key=True)
    Fecha = models.CharField(max_length=30)
    Coste = models.IntegerField()
    Abono = models.IntegerField()
    Restante = models.IntegerField()
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pedidos")
    Dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name="pedidos")
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Orden #{self.N_Orden}"

    class Meta:
        verbose_name_plural = "Pedidos"

# 🛠️ Modelo para reparaciones históricas
class Reparacion(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_orden = models.CharField(max_length=20)
    fecha_ingreso = models.DateField()
    rut = models.CharField(max_length=12)
    marca = models.CharField(max_length=50)
    equipo = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=50,
        choices=[
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
            ('pendiente', 'Pendiente'),
            ('entregado', 'Entregado'),
        ]
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.numero_orden}"

    class Meta:
        verbose_name_plural = "Reparaciones"
