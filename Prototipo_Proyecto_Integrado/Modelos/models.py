from django.db import models

# Create your models here.
class Cliente(models.Model):
    Nombre = models.CharField(max_length=20)
    Apellido = models.CharField(max_length=20)
    Numero_telefono= models.CharField(max_length=15)
    Direccion = models.CharField(max_length=50)
    Rut = models.IntegreField()
    Activo = models.BooleanField(default=True)
    def __str__(self):
        return self.Rut
    
class Pedido(models.Model):
    N_Orden = models.IntegerField()
    Fecha = models.CharField(max_length=30)
    Coste = models.IntegerField()
    Abono = models.IntegerField()
    Restante = models.IntegerField()
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Activo = models.BooleanField(default=True)
    def __str__(self):
        return self.N_Orden
    
class Marca(models.Model):
    Marca = models.CharField(max_length=20)
    def __str__(self):
        return self.Marca
    
class Modelo(models.Model):
    Modelo = models.CharField(max_length=50)
    Marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    def __str__(self):
        return self.Modelo

class Dispositivo(models.Model):
    Nombre = models.CharField(max_length=30)
    Trabajo_realizado = models.CharField(max_length=100)
    Codigo_Bloqueo = models.CharField(max_length=50)
    modelo = models.ForeignKey(Modelo,on_delete=models.CASCADE)
    Activo = models.BooleanField(default=True)
    def __str__(self):
        return self.Nombre