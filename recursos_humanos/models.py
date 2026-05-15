from django.db import models


# Create your models here.
class Evaluacion(models.Model):

    AREAS = [
        ('Tecnologia', 'Tecnología'),
        ('Calidad', 'Calidad'),
        ('Contabilidad', 'Contabilidad'),
        ('Tesoreria', 'Tesorería'),
        ('Costos', 'Costos'),
        ('Financiera', 'Financiera'),
    ]

    nombre = models.CharField(max_length=200)
    documento = models.CharField(max_length=50)
    correo = models.EmailField()

    area = models.CharField(
        max_length=20,
        choices=AREAS,
        default='Tecnologia'
    )

    cargo = models.CharField(max_length=100)

    puntaje = models.IntegerField(default=0)

    aprobado = models.BooleanField(default=False)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre