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


class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"


class vacantes(models.Model):
    cargo = models.CharField(max_length=50)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.IntegerField()
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    cv = models.FileField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
