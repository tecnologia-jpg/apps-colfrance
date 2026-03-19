from django.contrib import admin
from django.utils.html import format_html
from .models import Aforo, ModelSoporte

# Register your models here.


@admin.register(Aforo)
class AforoAdmin(admin.ModelAdmin):
    readonly_fields = ("preview_imagen",)
    list_display = ("id", "num_silo", "altura", "preview_imagen")
    search_fields = ("id",)
    list_filter = ("id",)

    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="200" style="border-radius:10px;" />',
                obj.imagen.url,
            )
        return "No hay imagen"

    preview_imagen.short_description = "Vista previa"


@admin.register(ModelSoporte)
class ModelSoporteAdmin(admin.ModelAdmin):
    # readonly_fields = ("",)
    list_display = ("id", "tipo_solicitud")
    search_fields = ("tipo_solicitud",)
    list_filter = ("tipo_solicitud",)
