from django.db import models


class Colaborador(models.Model):
    documento = models.CharField(
        max_length=20, unique=True, verbose_name="Numero de documento"
    )
    nombre = models.CharField(max_length=150, verbose_name="Nombre Completo")

    def __str__(self):
        return f"{self.nombre} - {self.documento}"


class Evaluacion(models.Model):
    # Tipos de exámenes disponibles
    EXAMENES = [
        ("limpieza", "Limpieza y Desinfección"),
        ("bph", "Buenas Prácticas Higiénicas (BPH)"),
    ]

    AREAS = [
        ("Tecnologia", "Tecnología"),
        ("Calidad", "Calidad"),
        ("Contabilidad", "Contabilidad"),
        ("Tesoreria", "Tesorería"),
        ("Costos", "Costos"),
        ("Financiera", "Financiera"),
    ]

    # --- NUEVO CAMPO ---
    tipo_examen = models.CharField(max_length=50, choices=EXAMENES, default="limpieza")

    # Campos que ya tenías
    nombre = models.CharField(max_length=200)
    documento = models.CharField(max_length=50)
    correo = models.EmailField()
    area = models.CharField(max_length=20, choices=AREAS, default="Tecnologia")
    cargo = models.CharField(max_length=100)
    puntaje = models.IntegerField(default=0)
    aprobado = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_examen_display()}"

    # --- NUEVOS MODELOS PARA EXÁMENES DINÁMICOS ---


class Examen(models.Model):
    nombre = models.CharField(max_length=200, help_text="Ej: Limpieza y Desinfección")
    puntaje_minimo = models.IntegerField(default=7)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Pregunta(models.Model):
    OPCIONES_CORRECTAS = [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]

    examen = models.ForeignKey(
        Examen, on_delete=models.CASCADE, related_name="preguntas"
    )
    numero = models.IntegerField(help_text="Número de la pregunta (1, 2, 3...)")
    texto = models.TextField(help_text="Texto de la pregunta")

    opcion_a = models.CharField(max_length=255)
    opcion_b = models.CharField(max_length=255)
    opcion_c = models.CharField(max_length=255, blank=True, null=True)  # Opcional
    opcion_d = models.CharField(max_length=255, blank=True, null=True)  # Opcional

    respuesta_correcta = models.CharField(max_length=1, choices=OPCIONES_CORRECTAS)

    class Meta:
        ordering = ["numero"]

    def __str__(self):
        return f"{self.numero}. {self.texto}"
