from django.db import models

# Create your models here.
class Cliente(models.Model):
    Nombre = models.CharField(max_length=20)
    Apellido = models.CharField(max_length=20)
    Numero_telefono= models.CharField(max_length=15)
    Direccion = models.CharField(max_length=50)
    Rut = models.IntegreField()

    def __str__(self):
        return self.Rut
    
class Pedido(models.Model):
    N_Orden = models.IntegerField()
    Fecha = models.CharField(max_length=30)
    Coste = models.IntegerField()
    Abono = models.IntegerField()
    Restante = models.IntegerField()
    def __str__(self):
        return self.N_Orden
    
