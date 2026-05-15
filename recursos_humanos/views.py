import os
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.db.models import Avg, Count, Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import openpyxl
from openpyxl.styles import Font, Alignment

from .forms import EvaluacionForm
from .models import Evaluacion

PATH_TEMPLATES_WEB = "recursos_humanos/views/"

# Respuestas del examen
RESPUESTAS_CORRECTAS = {
    'p1': 'B', 'p2': 'E', 'p3': 'B', 'p4': 'D', 'p5': 'C',
    'p6': 'A', 'p7': 'A', 'p8': 'B', 'p9': 'C', 'p10': 'D',
}

def index(request):
    """Vista del cuestionario con calificación inmediata."""
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            
            # Calificación
            puntaje = 0
            feedback = []
            for key, correcta in RESPUESTAS_CORRECTAS.items():
                r_usuario = request.POST.get(key)
                es_correcta = r_usuario == correcta
                if es_correcta: puntaje += 1
                
                feedback.append({
                    'pregunta': key,
                    'r_usuario': r_usuario,
                    'correcta': correcta,
                    'es_correcta': es_correcta
                })

            evaluacion.puntaje = puntaje
            evaluacion.aprobado = puntaje >= 7
            evaluacion.save()

            if evaluacion.aprobado:
                enviar_certificado_email(evaluacion)

            return render(request, f"{PATH_TEMPLATES_WEB}resultado.html", {
                'evaluacion': evaluacion,
                'feedback': feedback
            })
    else:
        form = EvaluacionForm()
    return render(request, f"{PATH_TEMPLATES_WEB}index.html", {"form": form})

def dashboard(request):
    """Dashboard con filtros, KPIs y gráficos con nombres legibles."""
    query = request.GET.get('q', '')
    area_filter = request.GET.get('area', '')
    
    datos = Evaluacion.objects.all().order_by('-fecha')
    
    if query:
        datos = datos.filter(Q(nombre__icontains=query) | Q(documento__icontains=query))
    if area_filter:
        datos = datos.filter(area=area_filter)

    # KPIs
    total = datos.count()
    aprobados = datos.filter(aprobado=True).count()
    reprobados = total - aprobados
    porcentaje = (aprobados / total * 100) if total > 0 else 0
    promedio = datos.aggregate(Avg('puntaje'))['puntaje__avg'] or 0

    # Gráficos: Mapeo de nombres técnicos a legibles
    conteo_areas = datos.values('area').annotate(total=Count('id'))
    area_map = dict(Evaluacion.AREAS) # Convierte la lista de CHOICES en un diccionario
    
    labels_areas = [area_map.get(item['area'], item['area']) for item in conteo_areas]
    data_areas = [item['total'] for item in conteo_areas]
    
    context = {
        'datos': datos,
        'total': total,
        'aprobados': aprobados,
        'reprobados': reprobados,
        'porcentaje': round(porcentaje, 1),
        'promedio': round(promedio, 1),
        'labels_areas': labels_areas,
        'data_areas': data_areas,
        'chart_pie_data': [aprobados, reprobados],
        'areas_choices': Evaluacion.AREAS,
        'query': query,
        'area_sel': area_filter
    }
    return render(request, f"{PATH_TEMPLATES_WEB}dashboard.html", context)

# --- UTILIDADES ---
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import cm
import os
import os
from io import BytesIO

import os
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

import os
from io import BytesIO
from django.conf import settings  # Importante para las rutas
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas


from io import BytesIO
from django.conf import settings
import os

from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse


from django.template.loader import render_to_string
from django.conf import settings

import os
from io import BytesIO
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader # Importante para procesar la imagen

import os
from io import BytesIO
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import os
from io import BytesIO
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def generar_pdf_buffer(evaluacion):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # --- 1. MARCOS (Basados en tu imagen) ---
    p.setStrokeColorRGB(0.05, 0.2, 0.7) # Azul
    p.setLineWidth(12)
    p.rect(15, 15, width-30, height-30, fill=0, stroke=1)
    
    p.setStrokeColorRGB(1, 0.5, 0) # Naranja
    p.setLineWidth(3)
    p.rect(28, 28, width-56, height-56, fill=0, stroke=1)

    # --- 2. EL LOGO (SOLUCIÓN DE RUTA) ---
    # Intentaremos tres formas de encontrar la imagen para que no falle:
    logo_path_escritorio = r"C:\Users\nocua\Desktop\apps-colfrance\apps_colfrance\static\images\colfrance.png"
    logo_path_proyecto = os.path.join(settings.BASE_DIR, 'static', 'images', 'colfrance.png')
    
    logo_final = None
    if os.path.exists(logo_path_proyecto):
        logo_final = logo_path_proyecto
    elif os.path.exists(logo_path_escritorio):
        logo_final = logo_path_escritorio

    if logo_final:
        try:
            # Usamos ImageReader para asegurar la lectura del PNG
            img = ImageReader(logo_final)
            # Ajustamos la posición para que quede centrado arriba
            p.drawImage(img, width/2 - 75, height - 150, width=150, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            # Si falla la imagen, al menos ponemos el nombre para que no salga vacío
            p.setFont("Helvetica-Bold", 20)
            p.drawCentredString(width/2, height - 100, "COLFRANCE S.A.")
            print(f"Error al dibujar imagen: {e}")
    else:
        # Texto de respaldo si el archivo no existe físicamente
        p.setFont("Helvetica-Bold", 25)
        p.setFillColorRGB(0.05, 0.2, 0.7)
        p.drawCentredString(width/2, height - 110, "COLFRANCE S.A.")

    # --- 3. TEXTOS DEL CERTIFICADO ---
    p.setFont("Helvetica-Bold", 42)
    p.setFillColorRGB(0.05, 0.2, 0.7)
    p.drawCentredString(width/2, height - 230, "CERTIFICADO DE LOGRO")

    # Nombre del empleado
    p.setFont("Helvetica-Bold", 35)
    p.setFillColor(colors.black)
    p.drawCentredString(width/2, height - 320, str(evaluacion.nombre).upper())

    p.setFont("Helvetica", 16)
    p.drawCentredString(width/2, height - 370, "Por haber aprobado satisfactoriamente la evaluación técnica de:")
    
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width/2, height - 410, "LIMPIEZA Y DESINFECCIÓN")

    # --- 4. SELLO DE PUNTAJE ---
    p.setStrokeColorRGB(0.05, 0.2, 0.7)
    p.setLineWidth(2)
    p.circle(width - 120, 130, 55, stroke=1, fill=0)
    
    p.setFont("Helvetica-Bold", 35)
    p.drawCentredString(width - 120, 125, str(evaluacion.puntaje))
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width - 120, 100, "PUNTOS")

    # --- 5. FIRMA Y FECHA ---
    p.setStrokeColor(colors.black)
    p.setLineWidth(1.5)
    p.line(width/2 - 120, 110, width/2 + 120, 110)
    
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width/2, 95, "GESTIÓN HUMANA / COLFRANCE S.A.")
    
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width/2, 70, f"Expedido el {evaluacion.fecha.strftime('%d de %B de %Y')}")

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def enviar_certificado_email(evaluacion):
    pdf = generar_pdf_buffer(evaluacion)
    email = EmailMessage(
        'Certificado de Aprobación - RRHH',
        f'Felicidades {evaluacion.nombre}, adjuntamos tu certificado.',
        to=[evaluacion.correo]
    )
    email.attach(f'Certificado_{evaluacion.documento}.pdf', pdf, 'application/pdf')
    email.send()

def descargar_pdf(request, id):
    evaluacion = get_object_or_404(Evaluacion, id=id)
    pdf = generar_pdf_buffer(evaluacion)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Certificado_{evaluacion.documento}.pdf"'
    return response

def exportar_excel(request):
    """Exporta evaluaciones con formato profesional."""
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Evaluaciones.xlsx"'
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Evaluaciones"
    
    # Encabezados en negrita
    headers = ['Nombre', 'Documento', 'Correo', 'Área', 'Cargo', 'Puntaje', 'Aprobado', 'Fecha']
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
    
    area_map = dict(Evaluacion.AREAS)
    
    for d in Evaluacion.objects.all():
        # Usamos el mapeo para que el Excel diga "Tecnología" y no "Tecnologia"
        nombre_area = area_map.get(d.area, d.area)
        ws.append([
            d.nombre, 
            d.documento, 
            d.correo, 
            nombre_area, 
            d.cargo, 
            d.puntaje, 
            "SI" if d.aprobado else "NO", 
            d.fecha.replace(tzinfo=None)
        ])
    
    # Ajustar ancho de columnas automáticamente
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except: pass
        ws.column_dimensions[column].width = max_length + 2

    wb.save(response)
    return response