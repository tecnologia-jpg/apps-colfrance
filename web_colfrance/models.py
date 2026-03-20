from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    emoji = models.CharField(max_length=1)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.URLField(blank=True, null=True)
    tabla_nutricional = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre
