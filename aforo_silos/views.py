from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout, authenticate, login as auth_login
from .services.data_silos import DataSilos
from pathlib import Path
from .models import Aforo, ModelSoporte
from django.forms.models import model_to_dict
from django.contrib import messages


RUTA_ACTUAL = Path(__file__).resolve()
# print(ruta_actual)
RUTA_PADRE = RUTA_ACTUAL.parent
# print(ruta_padre)
RUTA_ARCHIVO = RUTA_PADRE / "static" / "docs" / "programa_silos_maestro.xlsx"
# print(RUTA_ARCHIVO)
PATH_TEMPLATES_SILOS = "aforo_silos/views/"
# print(RUTA_ARCHIVO)
# if RUTA_ARCHIVO.exists():
#     print("funciona")


# recuperar registros del silo
def obtener_registros(id):
    obj = Aforo.objects.get(id=id)
    return obj


data = DataSilos.recuperar_datos(RUTA_ARCHIVO)


# Create your views here.
def principal(request):
    return render(request, f"{PATH_TEMPLATES_SILOS}login.html")


def login(request):
    context = {}

    # logica de acceso
    if request.method == "POST":

        nombre = request.POST.get("nombre")
        contrasena = request.POST.get("contraseña")
        user = authenticate(request, username=nombre, password=contrasena)
        if user is not None:
            auth_login(request, user)
            return redirect("aforo_silos:modulos")
        messages.error(request, "Usuario contraseña invalidos")

    return render(request, f"{PATH_TEMPLATES_SILOS}login.html", context)

    # redireccion silos
    # # return render(request, "aforo_silos/views/principal.html", context=context)

    # return render(request, "aforo_silos/views/principal.html", context=context)


def modulos(request):
    if request.method == "POST":

        rg_aforo = request.POST.get("modulo_registro")
        ver_rg_aforo = request.POST.get("modulo_ver_registros")
        soporte = request.POST.get("modulo_soporte")

        if rg_aforo:
            return redirect("aforo_silos:modulo_registro")
        if ver_rg_aforo:
            return redirect("aforo_silos:modulo_ver_registros")
        if soporte:
            return redirect("aforo_silos:modulo_soporte")

    return render(request, f"{PATH_TEMPLATES_SILOS}modulos.html")


def modulo_registro(request):
    context = {}
    context["silos"] = range(1, 21)
    context["data"] = data

    if request.method == "POST":
        mensaje = ""
        silo = request.POST.get("silo")
        centimetros = request.POST.get("centimetros")
        densidad = request.POST.get("densidad")
        total_kg = request.POST.get("total_kg")
        litros_calculados = request.POST.get("litros_calculados")
        capacidad_silo = request.POST.get("capacidad_silo")
        imagen = request.FILES.get("imagen")
        porcentaje_llenado = request.POST.get("porcentaje_llenado")
        ltr_disponible = request.POST.get("ltr_disponible")
        print(
            f"""
----- DATOS RECIBIDOS -----
Silo: {silo}
Centímetros: {centimetros}
Densidad: {densidad}
Total KG: {total_kg}
Litros calculados: {litros_calculados}
Capacidad silo: {capacidad_silo}
Imagen: {imagen}
Porcentaje llenado: {porcentaje_llenado}
Litros disponibles: {ltr_disponible}
---------------------------
"""
        )
        if imagen:
            registrar_aforo = Aforo(
                num_silo=silo,
                altura=centimetros,
                densidad=densidad,
                vol_litros=litros_calculados,
                kg_total=total_kg,
                # capacidad total
                porcentage_llenado=porcentaje_llenado,
                lts_disponibles=ltr_disponible,
                imagen=imagen,
            )

            registrar_aforo.save()
            mensaje = "El registro fue creado"
        else:
            mensaje = "Algo ocurrio"
        context["mensaje"] = mensaje
        return render(
            request, f"{PATH_TEMPLATES_SILOS}modulo_registro.html", context=context
        )

    elif request.method == "GET":
        silo = request.GET.get("silo")
        if silo != None:
            centimetros = request.GET.get("centimetros")
            densidad = request.GET.get("densidad")
            centimetros = float(centimetros)
            densidad = float(densidad)
            litros_calculados = DataSilos.consultar_aforo(silo, centimetros, data)
            capacidad_silo = DataSilos.consultar_capacidad(RUTA_ARCHIVO, silo)
            # La consulta de litros venddria siendo el volumen
            total_kg = DataSilos.calcular_peso(densidad, litros_calculados)
            context["datos_consulta"] = {
                "litros_calculados": litros_calculados,
                "silo": silo,
                "centimetros": centimetros,
                "densidad": densidad,
                "total_kg": total_kg,
                "capacidad_silo": capacidad_silo,
                "porcentaje_llenado": (litros_calculados / capacidad_silo) * 100,
                "ltr_disponible": capacidad_silo - litros_calculados,
            }
            context["mensaje"] = " Datos encontrados"

        else:
            type(silo)
            print(
                "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                silo,
            )
            context["mensaje"] = "Sin datos"

        # la funcion devuekve la cantidad de litros

        return render(
            request, f"{PATH_TEMPLATES_SILOS}modulo_registro.html", context=context
        )
    else:
        return render(
            request, f"{PATH_TEMPLATES_SILOS}modulo_registro.html", context=context
        )


def modulo_ver_registros(request):
    context = {}
    data_aforo = Aforo.objects.all()
    context["registros"] = data_aforo
    # recordar, los datos se traen como atributos del objeto
    # print(context[1].altura)
    return render(
        request, f"{PATH_TEMPLATES_SILOS}modulo_ver_registros.html", context=context
    )


def modulo_ver_registro(request, id):
    context = {}
    data_registro = Aforo.objects.get(id=id)
    data_dict = model_to_dict(data_registro)
    print(data_dict)
    context["data_dict"] = data_dict
    context["data_registro"] = data_registro

    return render(
        request, f"{PATH_TEMPLATES_SILOS}modulo_ver_registro.html", context=context
    )


def modulo_soporte(request):
    context = {}
    registros = ModelSoporte.objects.all()
    context["registros"] = registros

    return render(
        request, f"{PATH_TEMPLATES_SILOS}modulo_soporte.html", context=context
    )


def modulo_soporte_registro(request):
    context = {}
    if request.method == "POST":
        tipo_solicitud = request.POST.get("tipo_solicitud")
        comentarios = request.POST.get("comentarios")
        soporte = ModelSoporte(tipo_solicitud=tipo_solicitud, comentarios=comentarios)

        soporte.save()
        messages.success(request, "Su soporte fue cargado a sistema")
        mensaje = "Su soporte fue cargado a sistema"
        context["mensaje"] = mensaje
        print("Guardado")
        print(context)
        # return render(
        #     request,
        #     f"{PATH_TEMPLATES_SILOS}modulo_soporte.html",
        #     context=context,
        # )
        return redirect("aforo_silos:modulo_soporte")

    return render(
        request, f"{PATH_TEMPLATES_SILOS}modulo_soporte_registro.html", context=context
    )


def modulo_soporte_respuesta(request, id):
    context = {}
    data = ModelSoporte.objects.get(id=id)
    context["respuesta"] = data
    return render(
        request, f"{PATH_TEMPLATES_SILOS}modulo_soporte.html", context=context
    )


def cerrar_sesion(request):
    logout(request)
    return redirect("aforo_silos:login")
