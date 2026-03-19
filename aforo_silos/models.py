from django.db import models


# Create your models here.
class Aforo(models.Model):
    # usuario
    num_silo = models.CharField(max_length=20)
    # registra la fecha de creación
    hora_registro = models.DateTimeField(auto_now_add=True)
    altura = models.FloatField()
    densidad = models.FloatField()
    vol_litros = models.FloatField()
    kg_total = models.FloatField()
    # capacidad total
    porcentage_llenado = models.FloatField()
    lts_disponibles = models.FloatField()
    imagen = models.ImageField(upload_to="imgs_evidencia/")

    def __str__(self):
        return self.num_silo

    class Meta:
        verbose_name_plural = "Aforos"


class ModelSoporte(models.Model):
    tipo_solicitud = models.CharField(max_length=50)
    comentarios = models.CharField(max_length=200)
    hora = models.DateTimeField(auto_now_add=True)
    respuesta = models.CharField(max_length=400)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return self.tipo_solicitud

    class Meta:
        verbose_name_plural = "Soporte"

