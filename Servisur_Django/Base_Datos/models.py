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


# 💻 Modelo para dispositivos registrados
class Dispositivo(models.Model):
    modelo = models.ForeignKey(Modelo, on_delete=models.SET_NULL, null=True, related_name="dispositivos")
    Codigo_Bloqueo = models.CharField(max_length=50)
    Activo = models.BooleanField(default=True)
    rut = models.ForeignKey(Cliente, on_delete=models.SET_NULL,null=True,related_name="dispositivos")

    def __str__(self):
        marca = self.modelo.Marca.Marca if self.modelo and self.modelo.Marca else "Sin marca"
        modelo = self.modelo.Modelo if self.modelo else "Sin modelo"
        return f"{marca} {modelo}"

    class Meta:
        verbose_name_plural = "Dispositivos"

# 📋 Modelo para pedidos (órdenes de reparación)
class Pedido(models.Model):
    ESTADOS = [
        ('REG', 'Registrado'),
        ('PRO', 'En proceso'),
        ('TER', 'Terminado'),
    ]
    N_Orden = models.AutoField(primary_key=True)
    Fecha = models.CharField(max_length=30)
    Coste = models.IntegerField()
    Abono = models.IntegerField()
    Restante = models.IntegerField()
    Dispositivo = models.ForeignKey(Dispositivo, on_delete=models.SET_NULL, related_name="pedidos")
    Activo = models.BooleanField(default=True)
    Estado = models.CharField(max_length=3, choices=ESTADOS, default='REG')
    Tipo_de_falla = models.models.CharField(max_length=50, null=False)


    def __str__(self):
        return f"Orden #{self.N_Orden}"

    class Meta:
        verbose_name_plural = "Pedidos"
