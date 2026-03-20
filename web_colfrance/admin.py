from django.contrib import admin
from .models import Categoria, Producto

# Register your models here.


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    list_filter = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "descripcion",
        "categoria",
        "imagen",
        "tabla_nutricional",
    )
    search_fields = ("nombre",)
    list_filter = ("nombre",)
