from django.db import models
from django.contrib.auth.models import User


class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Control(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha = models.DateField()
    realizado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    observaciones = models.TextField()

    def __str__(self):
        return f"Control {self.id} - Equipo: {self.equipo.nombre}"
