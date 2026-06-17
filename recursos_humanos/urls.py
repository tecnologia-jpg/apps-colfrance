from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_examenes, name='index'),
    
    # --- ESTA ES LA LÍNEA QUE CAMBIA ---
    path('examen/<int:examen_id>/', views.tomar_examen, name='tomar_examen'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('descargar_pdf/<str:id>', views.descargar_pdf, name='descargar_pdf'),
]