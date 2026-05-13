from django.urls import path, include
from . import views

app_name = "control_plagas"

urlpatterns = [
    path("", views.login_control, name="login_control"),
    path("dashboard_view", views.dashboard_view, name="dashboard_view"),
]