from django.contrib import admin
from .models import Evaluacion, Examen, Pregunta, Colaborador

# importacion y exportacion
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.register(Evaluacion)


# Esta clase permite agregar las preguntas EN LA MISMA PANTALLA del examen
class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1  # Muestra una fila vacía para agregar rápido


@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ["nombre", "puntaje_minimo", "activo"]
    inlines = [PreguntaInline]


###########################################################################
# Revisar logica
###########################################################################


# 1. Configuramos el recurso de Importación/Exportación para Colaborador
class ColaboradorResource(resources.ModelResource):
    class Meta:
        model = Colaborador
        # IMPORTANTE: Usamos el documento como llave para evitar duplicados al importar
        import_id_fields = ("documento",)
        # Campos que se incluirán en el archivo de Excel/CSV
        fields = ("documento", "nombre")


# 2. Registramos el modelo en el Panel de Administración
@admin.register(Colaborador)
class ColaboradorAdmin(ImportExportModelAdmin):
    resource_class = ColaboradorResource

    # Columnas que se mostrarán en la tabla principal del admin
    list_display = ("documento", "nombre")

    # Barra de búsqueda para encontrar colaboradores rápidamente por cédula o nombre
    search_fields = ("documento", "nombre")

    # Ordenar por defecto alfabéticamente por nombre
    ordering = ("nombre",)
