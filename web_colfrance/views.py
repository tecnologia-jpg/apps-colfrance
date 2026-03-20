from django.shortcuts import render, redirect, HttpResponse
from pathlib import Path
import os
from .models import Producto, Categoria


def recuperar_imagenes_socios():
    path = r"apps_colfrance\static\web_colfrance\icons"
    imagenes = []

    if os.path.exists(path):
        for archivo in os.listdir(path):
            imagenes.append(archivo)
    return imagenes


RUTA_ACTUAL = Path(__file__).resolve()
# print(ruta_actual)
RUTA_PADRE = RUTA_ACTUAL.parent
# print(ruta_padre)

# print(RUTA_ARCHIVO)
PATH_TEMPLATES_SILOS = "web_colfrance/views/"
# print(RUTA_ARCHIVO)

# Create your views here.


def principal(request):
    context = {}
    categorias = Categoria.objects.all()
    context["categorias"] = categorias
    productos = Producto.objects.all()
    context["productos"] = productos
    print(context["productos"][1].__dict__)
    context["icons_socios"] = recuperar_imagenes_socios()
    print(context["icons_socios"])
    return render(request, f"{PATH_TEMPLATES_SILOS}principal.html", context=context)
