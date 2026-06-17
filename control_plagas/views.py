from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from pathlib import Path
import os
from django.contrib import messages
import json
from django.db.models import Count, Q
from .models import RegistroPlagas, ChatTicket, TicketPlaga
from recursos_humanos.models import Colaborador
from django.utils import timezone


# revisar esta funcion de descoradores
from .decorators import admin_o_colaborador_required

# librerias para inicio de sesion
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


RUTA_ACTUAL = Path(__file__).resolve()
RUTA_PADRE = RUTA_ACTUAL.parent
PATH_TEMPLATES_WEB = "control_plagas/views/"


# Create your views here.
def login_control(request):
    if request.user.is_authenticated:
        return redirect("control_plagas:dashboard_view")
    if request.method == "POST":
        user_val = request.POST.get("username")
        password_val = request.POST.get("password")

        user = authenticate(request, username=user_val, password=password_val)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("control_plagas:dashboard_view")
        else:
            messages.error(request, "Usuario o contraeña incorrectos:")

    return render(request, f"{PATH_TEMPLATES_WEB}login_control.html")


@login_required(login_url="control_plagas:login_control")
def dashboard_view(request):
    # admin_autenticado = request.user.is_authenticated
    # ejemplo_colab = request.session["colaborador"]
    # print(admin_autenticado)
    # print(ejemplo_colab)
    # 1. Traemos los reportes reales.
    # Usamos prefetch_related para que Django traiga los tickets asociados de una sola vez
    # y no haga cientos de consultas a la base de datos haciendo que el sistema se vuelva lento.
    reportes_queryset = RegistroPlagas.objects.prefetch_related(
        "ticketplaga_set"
    ).order_by("-fecha_hora")

    # 2. Cálculos de estadísticas generales
    total_reportes = reportes_queryset.count()
    areas_afectadas = reportes_queryset.values("area").distinct().count()
    clientes_unicos = reportes_queryset.values("cedula").distinct().count()

    # 3. CÁLCULO DE ESTADOS REALES (Usando el modelo TicketPlaga)
    # Asumimos que estado=True es Completado.
    completados = TicketPlaga.objects.filter(estado=True).count()

    # Los pendientes son todos los reportes a los que les restamos los ya completados
    # (Esto cubre los que tienen Ticket en estado=False y los que son tan nuevos que aún no tienen Ticket)
    pendientes = total_reportes - completados

    # (Opcional) Métrica extra: Cuántos chats/mensajes se han intercambiado en total
    total_mensajes = ChatTicket.objects.count()

    # 4. CONSTRUCCIÓN DE GRÁFICOS (CHART.JS) - Se mantiene igual
    plagas_query = RegistroPlagas.objects.values("plaga").annotate(total=Count("id"))
    data_plagas = {item["plaga"]: item["total"] for item in plagas_query}

    areas_query = RegistroPlagas.objects.values("area").annotate(total=Count("id"))
    dict_areas_labels = dict(RegistroPlagas.OPCIONES_AREA)
    data_areas = {
        dict_areas_labels.get(item["area"], item["area"]): item["total"]
        for item in areas_query
    }

    severidad_query = RegistroPlagas.objects.values("prioridad").annotate(
        total=Count("id")
    )
    data_severidad = {item["prioridad"]: item["total"] for item in severidad_query}

    # 5. Enviamos el contexto
    context = {
        "reportes": reportes_queryset,
        "total_reportes": total_reportes,
        "pendientes": pendientes,
        "completados": completados,
        "areas_afectadas": areas_afectadas,
        "clientes_unicos": clientes_unicos,
        "total_mensajes": total_mensajes,  # Nueva métrica
        "json_plagas": json.dumps(data_plagas),
        "json_areas": json.dumps(data_areas),
        "json_severidad": json.dumps(data_severidad),
    }

    return render(request, f"{PATH_TEMPLATES_WEB}dashboard.html", context)


@admin_o_colaborador_required
def view_form(request):
    if request.method == "POST":
        cedula_val = request.POST.get("cedula")
        fecha_hora_val = request.POST.get("fecha_hora")
        area_val = request.POST.get("area")
        prioridad_val = request.POST.get("prioridad")
        tipo_plaga_val = request.POST.get("tipo_plaga")
        plaga_val = request.POST.get("plaga")
        descripcion_val = request.POST.get("descripcion")
        evidencia_val = request.FILES.get("evidencia")
        nuevo_registro = RegistroPlagas(
            cedula=cedula_val,
            area=area_val,
            tipo_plaga=tipo_plaga_val,
            plaga=plaga_val,
            prioridad=prioridad_val,
            descripcion=descripcion_val,
            evidencia=evidencia_val,
        )
        nuevo_registro.save()
        messages.success(request, "¡Reporte de plaga registrado exitosamente!")
        if request.user.is_authenticated:
            return redirect("control_plagas:dashboard_view")
        elif request.session == "colaborador":
            return redirect("control_plagas:dashboard_colaborador")
    # else:
    #     messages.error(request, "¡Reporte de plaga registrado exitosamente!")
    #     print("PAso algun error")
    #     return redirect("control_plagas:dashboard_view")

    return render(request, f"{PATH_TEMPLATES_WEB}form.html")


@login_required(login_url="control_plagas:login_control")
def reportesTK_view(request):
    # Traemos todos los reportes y cruzamos con sus tickets para la tabla
    reportes = (
        RegistroPlagas.objects.prefetch_related("ticketplaga_set")
        .all()
        .order_by("-fecha_hora")
    )
    return render(
        request, f"{PATH_TEMPLATES_WEB}reportesTK.html", {"reportes": reportes}
    )
    ############################################################
    """
    Apartado de colaboradores.
    """


# @login_required(login_url="control_plagas:login_control")
def detalle_ticket_view(request, reporte_id):
    # 1. ¿QUIÉN ESTÁ ENTRANDO?
    es_admin = request.user.is_authenticated
    es_colaborador = "colaborador" in request.session

    print(f"Colaborador {es_colaborador}")
    print(f"ADMIN {es_admin}")
    # Si no es ninguno de los dos, lo echamos (por seguridad)
    if not es_admin and not es_colaborador:
        messages.warning(request, "Debes iniciar sesión para ver este ticket.")
        return redirect("control_plagas:login_colab")  # O al login que prefieras

    # 2. Obtenemos el reporte y el ticket
    reporte = get_object_or_404(RegistroPlagas, id=reporte_id)

    # IMPORTANTE: Si es colaborador, validamos que el reporte sea SUYO
    if es_colaborador and reporte.cedula != request.session["colaborador"]["documento"]:
        messages.error(request, "No tienes permiso para ver este ticket.")
        return redirect("control_plagas:dashboard_colaborador")

    # Buscamos o creamos el ticket
    ticket, created = TicketPlaga.objects.get_or_create(
        registro=reporte,
        defaults={
            "estado": False,
            "hora_inicio": timezone.now(),
            "hora_final": timezone.now(),
            "descripcion_solucion": "",
            "usuario_asignado": (
                request.user if es_admin else None
            ),  # Solo se asigna si quien lo abre es Admin
        },
    )

    if "colaborador" in request.session:
        usuario_val = request.session.get("colaborador")
        usuario_val_ = usuario_val["nombre"]
        usuario_rol_val = "colaborador"
    else:
        usuario_val = request.user.username
        usuario_rol_val = "administrador"

    print(usuario_val)

    # 3. PROCESAMIENTO DEL POST (Formularios)
    if request.method == "POST":

        # A. Chat (AMBOS pueden enviar mensajes si no está cerrado)
        if "enviar_mensaje" in request.POST and not ticket.estado:
            texto = request.POST.get("mensaje")
            archivo = request.FILES.get("media")

            if texto or archivo:
                # Opcional: Podrías agregar un campo en ChatTicket para saber quién lo envió
                ChatTicket.objects.create(
                    ticket=ticket,
                    fecha=timezone.now(),
                    mensaje=texto,
                    media=archivo,
                    usuario=usuario_val,
                    usuario_rol=usuario_rol_val,
                )
                messages.success(request, "Mensaje enviado.")
            return redirect("control_plagas:detalle_ticket", reporte_id=reporte.id)

        # B. Cambio de Estado (SOLO ADMIN)
        elif "cambiar_estado" in request.POST and es_admin:
            nuevo_estado = request.POST.get("nuevo_estado") == "True"
            ticket.estado = nuevo_estado
            if nuevo_estado:
                ticket.hora_final = timezone.now()
                ticket.descripcion_solucion = request.POST.get(
                    "descripcion_solucion", ""
                )
            ticket.save()
            messages.success(request, "Estado del ticket actualizado.")
            return redirect("control_plagas:detalle_ticket", reporte_id=reporte.id)

    # 4. Renderizamos enviando el rol al HTML
    mensajes = ChatTicket.objects.filter(ticket=ticket).order_by("fecha")

    context = {
        "reporte": reporte,
        "ticket": ticket,
        "mensajes": mensajes,
        "es_admin": es_admin,  # Pasamos esta variable a la plantilla
    }
    # print("Mensajes) ", context["mensajes"][0].usuario)
    # print("xxxxx"
    return render(request, f"{PATH_TEMPLATES_WEB}detalle_ticket.html", context)


def login_colab(request):
    if request.method == "POST":
        documento_val = request.POST.get("documento")
        # print(documento_val)

        colaborador = Colaborador.objects.filter(documento=documento_val).first()
        if colaborador:
            request.session["colaborador"] = {
                "nombre": colaborador.nombre,
                "documento": colaborador.documento,
            }
            return redirect("control_plagas:dashboard_colaborador")

        messages.success(request, f"el docuemtno es {documento_val}")
        # redirect("control_plagas:login_colab")
    return render(request, f"{PATH_TEMPLATES_WEB}login_colab.html")


# @colaborador_required
def dashboard_colaborador(request):
    context = {}
    es_admin = request.user.is_authenticated
    es_colaborador = "colaborador" in request.session

    print(f"Colaborador {es_colaborador}")
    print(f"ADMIN {es_admin}")
    colaborador = request.session.get("colaborador")
    reportes = RegistroPlagas.objects.filter(cedula=colaborador["documento"])
    context["reportes"] = reportes
    print(reportes)
    print(colaborador)
    return render(
        request, f"{PATH_TEMPLATES_WEB}dashboard_colaborador.html", context=context
    )


#########################################################################################
# Cerrar Sesion
#########################################################################################


# cierre de sesion para admin
def logout_control(request):

    logout(request)
    messages.info(request, "Cerrada la Sesion")
    return redirect("control_plagas:login_control")


def logout_colab(request):
    if "colaborador" in request.session:
        del request.session["colaborador"]

    messages.info(request, "Cerrada la Session del Colaborador")
    return redirect("control_plagas:login_colab")
