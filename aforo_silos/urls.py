from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "aforo_silos"

urlpatterns = [
    path("", views.principal, name="principal"),
    path("login", views.login, name="login"),
    path("modulos", views.modulos, name="modulos"),
    path("modulo_registro", views.modulo_registro, name="modulo_registro"),
    path(
        "modulo_ver_registros", views.modulo_ver_registros, name="modulo_ver_registros"
    ),
    path(
        "modulo_ver_registro/<int:id>",
        views.modulo_ver_registro,
        name="modulo_ver_registro",
    ),
    path(
        "modulo_soporte/",
        views.modulo_soporte,
        name="modulo_soporte",
    ),
    path(
        "modulo_soporte_registro/",
        views.modulo_soporte_registro,
        name="modulo_soporte_registro",
    ),
    path(
        "cerrar_sesion/",
        views.cerrar_sesion,
        name="cerrar_sesion",
    ),
]
