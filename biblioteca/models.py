from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    dni = models.CharField(max_length=9)
    direccion = models.EmailField()
    telefono = models.IntegerField()
    pass
    def __str__(self):
        return self.dni

class Autor(models.Model):
    nombre = models.CharField(max_length=20)
    biografia = models.TextField()
    foto = models.ImageField()

class Editorial(models.Model):
    nombre = models.CharField(max_length=20)
    direccion = models.CharField(max_length=30)
    sitioWeb = models.URLField()


class Libro(models.Model):
    titulo = models.CharField(max_length=30)
    autor = Autor
    editorial = Editorial
    fechaPublicacion = models.DateField()
    genero = models.CharField(max_length=10)
    isbn = models.CharField(max_length=20)
    resumen = models.TextField()
    disponibilidad = models.CharField(max_length=20)
    portada = models.ImageField()