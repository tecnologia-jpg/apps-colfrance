from django.shortcuts import render, redirect, HttpResponse
from pathlib import Path
import os
from django.contrib import messages
import json




RUTA_ACTUAL = Path(__file__).resolve()
RUTA_PADRE = RUTA_ACTUAL.parent
PATH_TEMPLATES_WEB = "control_plagas/views/"


# Create your views here.
def login_control(request):
    return render(request, f"{PATH_TEMPLATES_WEB}login_control.html")
    



def dashboard_view(request):
    # Datos ficticios simulando una consulta a la base de datos
    reportes = [
        {'id': 1, 'area': 'Cocina', 'tipoPlaga': 'Roedores', 'severidad': 'Alta', 'estado': 'pendiente'},
        {'id': 2, 'area': 'Almacén', 'tipoPlaga': 'Cucarachas', 'severidad': 'Media', 'estado': 'completado'},
        {'id': 3, 'area': 'Jardín', 'tipoPlaga': 'Hormigas', 'severidad': 'Baja', 'estado': 'completado'},
        {'id': 4, 'area': 'Cocina', 'tipoPlaga': 'Cucarachas', 'severidad': 'Alta', 'estado': 'pendiente'},
        {'id': 5, 'area': 'Oficinas', 'tipoPlaga': 'Termitas', 'severidad': 'Media', 'estado': 'pendiente'},
    ]

    # Cálculos de estadísticas
    total_reportes = len(reportes)
    pendientes = len([r for r in reportes if r['estado'] == 'pendiente'])
    completados = len([r for r in reportes if r['estado'] == 'completado'])
    areas_afectadas = len(set(r['area'] for r in reportes))
    clientes_unicos = 12 # Dato estático de ejemplo

    # Preparar datos para los gráficos (JSON para JavaScript)
    data_plagas = {'Cucarachas': 2, 'Roedores': 1, 'Hormigas': 1, 'Termitas': 1}
    data_areas = {'Cocina': 2, 'Almacén': 1, 'Jardín': 1, 'Oficinas': 1}
    data_severidad = {'Alta': 2, 'Media': 2, 'Baja': 1}

    context = {
        'total_reportes': total_reportes,
        'pendientes': pendientes,
        'completados': completados,
        'areas_afectadas': areas_afectadas,
        'clientes_unicos': clientes_unicos,
        # Pasamos los diccionarios como JSON strings
        'json_plagas': json.dumps(data_plagas),
        'json_areas': json.dumps(data_areas),
        'json_severidad': json.dumps(data_severidad),
    }
    return render(request, f"{PATH_TEMPLATES_WEB}dashboard.html")

