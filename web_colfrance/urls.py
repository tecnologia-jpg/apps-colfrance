from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "web_colfrance"

urlpatterns = [
    path(
        "",
        views.principal,
        name="principal",
    ),
    path(
        "cargar_datos_contacto",
        views.cargar_datos_contacto,
        name="cargar_datos_contacto",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
