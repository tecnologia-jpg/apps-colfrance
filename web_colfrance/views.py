from django.shortcuts import render, redirect, HttpResponse
from pathlib import Path
import os
from django.contrib import messages
from .models import Producto, Categoria, Contacto
from .forms import FormContacto


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
PATH_TEMPLATES_WEB = "web_colfrance/views/"
# print(RUTA_ARCHIVO)

# Create your views here.


def principal(request):
    context = {}
    categorias = Categoria.objects.all()
    print(categorias)
    productos = Producto.objects.all()
    print(productos)
    context["icons_socios"] = recuperar_imagenes_socios()
    print(context["icons_socios"])
    if categorias:
        context["categorias"] = categorias
    if productos:
        context["productos"] = productos
        # print(context["productos"][1].__dict__)

        return render(request, f"{PATH_TEMPLATES_WEB}principal.html", context=context)
    else:
        return render(request, f"{PATH_TEMPLATES_WEB}principal.html", context=context)


def cargar_datos_contacto(request):
    if request.method == "POST":
        form = FormContacto(request.POST)
        if form.is_valid():
            try:

                data = form.cleaned_data
                Contacto.objects.create(
                    nombre=data["nombre"],
                    correo=data["correo"],
                    telefono=data["telefono"],
                    asunto=data["asunto"],
                    mensaje=data["mensaje"],
                )

                print(" mensaje enviado")
                messages.success(request, "Mensaje enviado correctamente.")
                return redirect("web_colfrance:principal")

            except Exception as e:

                messages.error(request, f"Datos invalidos. {e}")
    else:
        error_msg = list(form.errors.values())[0][0]
        messages.error(request, f"Datos invalidos. {error_msg}")

        # print(nombre, email, telefono, mensaje)  # funcionando
        return redirect("web_colfrance:principal")

    return redirect("web_colfrance:principal")
