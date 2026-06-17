from django.db import models

# !!Importante - tabla de relacion de usuarios
from django.contrib.auth.models import User

# Create your models here.


class RegistroPlagas(models.Model):

    # 1. Opciones de Área del Hallazgo
    OPCIONES_AREA = [
        ("FERMENTOS", "Fermentos"),
        ("CAVAS", "Cavas"),
        ("MUELLE DE CARGA", "Muelle de Carga"),
        ("PASTEURIZACIÓN", "Pasteurización"),
        ("MEZCLAS", "Mezclas"),
        ("UHT", "UHT"),
        ("QUESERA", "Quesera"),
        ("BODEGA LOGISTICA", "Bodega Logística"),
        ("CUARTOS FRIOS PRODUCTO TERMINADO", "Cuartos Fríos Producto Terminado"),
        ("BODEGA MATERIA PRIMA", "Bodega Materia Prima"),
        ("ACOPIO RESIDUOS SÓLIDOS", "Acopio Residuos Sólidos"),
        ("PULVERIZADORA", "Pulverizadora"),
    ]

    # 2. Opciones de Tipo de Plaga
    OPCIONES_TIPO_PLAGA = [
        ("Rastreras", "Plagas rastreras"),
        ("Voladoras", "Plagas voladoras"),
        ("Roedoras", "Plagas roedoras"),
    ]

    # 3. Opciones de Plaga Específica (Agrupadas por tipo)
    OPCIONES_PLAGA = [
        (
            "Plagas rastreras",
            (
                ("Cucarachas", "Cucarachas"),
                ("Hormigas", "Hormigas"),
                ("Escarabajos", "Escarabajos"),
                ("Arañas", "Arañas"),
                ("Lepismas", "Lepismas (pececillos de plata)"),
            ),
        ),
        (
            "Plagas voladoras",
            (
                ("Moscas", "Moscas"),
                ("Mosquitos", "Mosquitos"),
                ("Polillas", "Polillas"),
                ("Avispas", "Avispas"),
                ("Abejas", "Abejas"),
            ),
        ),
        (
            "Plagas roedoras",
            (
                ("Ratón doméstico", "Ratón doméstico"),
                ("Rata gris", "Rata gris"),
                ("Rata negra", "Rata negra"),
            ),
        ),
    ]

    # Opciones de Prioridad (Mantenemos las estándar)
    OPCIONES_PRIORIDAD = [
        ("Alta", "Alta"),
        ("Media", "Media"),
        ("Baja", "Baja"),
    ]

    ### CAMPOS DEL MODELO ###
    cedula = models.CharField(max_length=20, verbose_name="Cédula del Reportante")

    # Aplicando los choices a los campos
    area = models.CharField(
        max_length=100, choices=OPCIONES_AREA, verbose_name="Área Afectada"
    )
    tipo_plaga = models.CharField(
        max_length=50, choices=OPCIONES_TIPO_PLAGA, verbose_name="Tipo de Plaga"
    )
    plaga = models.CharField(
        max_length=50, choices=OPCIONES_PLAGA, verbose_name="Plaga Específica"
    )
    prioridad = models.CharField(
        max_length=20, choices=OPCIONES_PRIORIDAD, verbose_name="Prioridad/Severidad"
    )

    descripcion = models.TextField(verbose_name="Descripción del Problema")
    # auto_now_add=True toma la fecha y hora exacta del servidor al momento de guardar
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    evidencia = models.FileField(
        upload_to="evidencias_plagas/",
        blank=True,
        null=True,
        verbose_name="Archivo de Evidencia",
    )

    def __str__(self):
        return f"Reporte: {self.plaga} en {self.get_area_display()} - Cédula: {self.cedula}"


class TicketPlaga(models.Model):
    registro = models.ForeignKey(
        RegistroPlagas, on_delete=models.CASCADE
    )  # campo de relacion
    usuario_asignado = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )  # campo de relacion
    estado = models.BooleanField()
    hora_inicio = models.DateTimeField()
    hora_final = models.DateTimeField()
    descripcion_solucion = models.TextField()


class ChatTicket(models.Model):
    ticket = models.ForeignKey(
        TicketPlaga, on_delete=models.CASCADE
    )  # campo de relacion
    fecha = models.DateTimeField()
    mensaje = models.CharField()
    media = models.FileField()
    usuario = models.CharField()
    usuario_rol = models.CharField()
