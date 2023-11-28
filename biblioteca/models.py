from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    dni = models.CharField(max_length=9, null=True)
    direccion = models.CharField(max_length=20, null=True)
    telefono = models.IntegerField(null=True)
    def __str__(self):
        return self.dni

class Autor(models.Model):
    nombre = models.CharField(max_length=20)
    biografia = models.TextField()
    foto = models.ImageField() 
    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    nombre = models.CharField(max_length=20)
    direccion = models.CharField(max_length=30)
    sitioWeb = models.URLField()
    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=30)
    autor = models.ManyToManyField(Autor)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    fechaPublicacion = models.DateField()
    genero = models.CharField(max_length=10)
    isbn = models.CharField(max_length=20)
    resumen = models.TextField()
    disponibilidad = models.CharField(max_length=20, choices=(
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('proceso', 'En proceso de prestamo'),
        ))
    portada = models.ImageField()
    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    libroPrestado = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fechaPrestamo = models.DateField()
    fechaDevolucion = models.DateField()
    usuarioPrestado = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estadoPrestamo = models.CharField(max_length=20)
