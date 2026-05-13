from django.db import models

# Create your models here.

class RegistroPlagas(models.Model):
    # operario
    importancia= models.CharField()
    tipo_plaga=models.CharField()
    descripcion= models.TextField()
    area= models.CharField
    fecha_hora = models.DateTimeField()
    estado=models.BooleanField()
    