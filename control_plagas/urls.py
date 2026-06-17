from django.urls import path, include
from . import views

app_name = "control_plagas"

urlpatterns = [
    path("", views.login_control, name="login_control"),
    path("dashboard_view", views.dashboard_view, name="dashboard_view"),
    path("view_form", views.view_form, name="view_form"),
    path(
        "reportesTK_view",
        views.reportesTK_view,
        name="reportesTK_view",
    ),  # urls.py (de tu aplicación)
    path("reporte/<int:reporte_id>/", views.detalle_ticket_view, name="detalle_ticket"),
    # Apartado de colaboradores
    path("login_colab", views.login_colab, name="login_colab"),
    path(
        "dashboard_colaborador",
        views.dashboard_colaborador,
        name="dashboard_colaborador",
    ),
    # cerrar sesion
    path("logout_control", views.logout_control, name="logout_control"),
    path("logout_colab", views.logout_colab, name="logout_colab"),
]
