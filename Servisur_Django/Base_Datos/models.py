from django.db import models
from django.contrib.auth.models import User

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


# 🏷️ Modelo para marcas de dispositivos
class Marca(models.Model):
    Marca = models.CharField(max_length=20)

    def __str__(self):
        return self.Marca


# 📦 Modelo para modelos de dispositivos
class Modelo(models.Model):
    Modelo = models.CharField(max_length=50)
    Marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
        return self.Modelo


# 💻 Modelo para dispositivos registrados
class Dispositivo(models.Model):
    Nombre = models.CharField(max_length=30)
    Trabajo_realizado = models.CharField(max_length=100)
    Codigo_Bloqueo = models.CharField(max_length=50)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return self.Nombre


# 📋 Modelo para pedidos (órdenes de reparación)
class Pedido(models.Model):
    N_Orden = models.AutoField(primary_key=True)
    Fecha = models.CharField(max_length=30)  # Puedes cambiar a DateField si quieres validación automática
    Coste = models.IntegerField()
    Abono = models.IntegerField()
    Restante = models.IntegerField()
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Orden #{self.N_Orden}"


# 🛠️ Modelo para reparaciones históricas
class Reparacion(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_orden = models.CharField(max_length=20)
    fecha_ingreso = models.DateField()
    rut = models.CharField(max_length=12)
    marca = models.CharField(max_length=50)
    equipo = models.CharField(max_length=100)
    estado = models.CharField(max_length=50, choices=[
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('pendiente', 'Pendiente'),
        ('entregado', 'Entregado'),
    ])

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.numero_orden}"
