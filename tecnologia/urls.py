from django.urls import path, include
from . import views

app_name = "tecnologia"


urlpatterns = [
    # 1. Nota el "/" al final de 'generar-acta/'
    # 2. Nota el nombre exacto que le diste: 'generar-acta' (con guion medio)
    path("generar-acta/", views.generar_acta_con_firma, name="generar-acta"),
]
