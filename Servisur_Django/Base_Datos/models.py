from django.db import models

# 🧍 Modelo para clientes
class Cliente(models.Model):
    ORIGEN_CHOICES = [
    ('NAC', 'Nacional'),
    ('EXT', 'Extranjero'),
    ]
    Origen = models.CharField(max_length=3,choices=ORIGEN_CHOICES,default='NAC')
    Nombre = models.CharField(max_length=20)
    Apellido = models.CharField(max_length=20)
    Numero_telefono = models.CharField(max_length=15,null=True)
    Rut = models.CharField(max_length=50)
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
    rut = models.ForeignKey(Cliente, on_delete=models.SET_NULL,null=True,related_name="dispositivos")
    Metodo_Bloqueo = models.CharField(max_length=6, choices=METODOS_CHOICES,default='PASS')
    Codigo_Bloqueo = models.CharField(max_length=50)
    

    def __str__(self):
        marca = self.modelo.Marca.Marca if self.modelo and self.modelo.Marca else "Sin marca"
        modelo = self.modelo.Modelo if self.modelo else "Sin modelo"
        return f"{marca} {modelo}"

    class Meta:
        verbose_name_plural = "Dispositivos"
        
class Tipo_Falla(models.Model):
    Falla = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# 📋 Modelo para pedidos (órdenes de reparación)
class Pedido(models.Model):
    ESTADOS = [
        ('REG', 'Registrado'),
        ('PRO', 'En proceso'),
        ('TER', 'Terminado'),
    ]
    N_Orden = models.AutoField(primary_key=True)
    Fecha = models.DateField()
    Coste = models.IntegerField()
    Abono = models.IntegerField()
    Restante = models.IntegerField()
    Dispositivo = models.ForeignKey(Dispositivo, on_delete=models.SET_NULL, null=True, related_name="pedidos")
    Activo = models.BooleanField(default=True)
    Estado = models.CharField(max_length=3, choices=ESTADOS, default='REG')
    Observaciones = models.CharField(max_length=50, null=True)
    Tipo_de_falla = models.ForeignKey(Tipo_Falla,on_delete=models.SET_NULL, null=True, related_name="pedidos")

    def __str__(self):
        return f"Orden #{self.N_Orden}"

    class Meta:
        verbose_name_plural = "Pedidos"
