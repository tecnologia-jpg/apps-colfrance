import os
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.db.models import Avg, Count, Q
from django.conf import settings

# ReportLab para PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

# OpenPyXL para Excel
import openpyxl
from openpyxl.styles import Font, Alignment

# Modelos y Formularios
from .forms import EvaluacionForm
from .models import Evaluacion, Examen, Pregunta # IMPORTANTE: Deben existir en models.py

# --- 1. CONFIGURACIONES GLOBALES ---
PATH_TEMPLATES_WEB = "recursos_humanos/views/"

# --- 2. VISTAS PRINCIPALES (DINÁMICAS) ---
def lista_examenes(request):
    """Muestra los exámenes activos desde la Base de Datos."""
    examenes_bd = Examen.objects.filter(activo=True)
    return render(request, f"{PATH_TEMPLATES_WEB}index.html", {
        'examenes': examenes_bd
    })

def tomar_examen(request, examen_id):
    """Vista dinámica que renderiza y califica desde la Base de Datos."""
    examen = get_object_or_404(Examen, id=examen_id, activo=True)

    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.tipo_examen = examen.nombre[:50] # Guardamos el nombre del examen
            
            puntaje = 0
            feedback = []
            
            # Calificamos comparando con la base de datos
            for pregunta in examen.preguntas.all():
                respuesta_usuario = request.POST.get(f"p{pregunta.id}")
                es_correcta = respuesta_usuario == pregunta.respuesta_correcta
                
                if es_correcta:
                    puntaje += 1
                
                feedback.append({
                    'pregunta': pregunta.texto,
                    'r_usuario': respuesta_usuario,
                    'correcta': pregunta.respuesta_correcta,
                    'es_correcta': es_correcta
                })

            evaluacion.puntaje = puntaje
            evaluacion.aprobado = puntaje >= examen.puntaje_minimo
            evaluacion.save()

            if evaluacion.aprobado:
                enviar_certificado_email(evaluacion)

            return render(request, f"{PATH_TEMPLATES_WEB}resultado.html", {
                'evaluacion': evaluacion,
                'feedback': feedback,
                'nombre_examen': examen.nombre
            })
    else:
        form = EvaluacionForm()
        
    # Usamos UNA SOLA PLANTILLA para todos los exámenes
    return render(request, f"{PATH_TEMPLATES_WEB}examen_dinamico.html", {
        "form": form,
        "examen": examen
    })

def dashboard(request):
    """Dashboard con filtros, KPIs y gráficos con nombres legibles."""
    query = request.GET.get('q', '')
    area_filter = request.GET.get('area', '')
    
    datos = Evaluacion.objects.all().order_by('-fecha')
    
    if query:
        datos = datos.filter(Q(nombre__icontains=query) | Q(documento__icontains=query))
    if area_filter:
        datos = datos.filter(area=area_filter)

    total = datos.count()
    aprobados = datos.filter(aprobado=True).count()
    reprobados = total - aprobados
    porcentaje = (aprobados / total * 100) if total > 0 else 0
    promedio = datos.aggregate(Avg('puntaje'))['puntaje__avg'] or 0

    conteo_areas = datos.values('area').annotate(total=Count('id'))
    area_map = dict(Evaluacion.AREAS)
    
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


# --- 3. UTILIDADES (PDF y EXCEL) ---
def generar_pdf_buffer(evaluacion):
    buffer = BytesIO()
    # Usamos tamaño carta en horizontal (792 x 612 puntos)
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # --- 1. FONDO Y MARCOS (CON GRADIENTE AZUL A ROJO) ---
    # Fondo color crema/hueso muy suave
    p.setFillColorRGB(0.96, 0.96, 0.94)
    p.rect(0, 0, width, height, fill=1, stroke=0)

    # Colores corporativos para el degradado
    r1, g1, b1 = 0.05, 0.2, 0.7  # Azul Colfrance (Izquierda)
    r2, g2, b2 = 0.8, 0.2, 0.3   # Rojo/Rosa (Derecha)

    # Marco exterior principal
    p.setLineWidth(5)

    # Línea Izquierda (Sólida Azul)
    p.setStrokeColorRGB(r1, g1, b1)
    p.line(15, 15, 15, height-15)

    # Línea Derecha (Sólida Roja)
    p.setStrokeColorRGB(r2, g2, b2)
    p.line(width-15, 15, width-15, height-15)

    # Líneas Superior e Inferior (Gradiente simulado matemáticamente)
    segments = 150
    seg_width = (width - 30) / segments
    for i in range(segments):
        frac = i / float(segments - 1)
        # Interpolar colores paso a paso
        r = r1 + (r2 - r1) * frac
        g = g1 + (g2 - g1) * frac
        b = b1 + (b2 - b1) * frac
        p.setStrokeColorRGB(r, g, b)
        
        x_start = 15 + (i * seg_width)
        x_end = x_start + seg_width + 1 # +1 para solapar y evitar huecos
        
        # Dibujar segmentos
        p.line(x_start, height-15, x_end, height-15) # Arriba
        p.line(x_start, 15, x_end, 15)               # Abajo

    # Esquinas decorativas internas (Más delgadas para contrastar elegantemente)
    p.setLineWidth(2)
    
    # Esquinas Izquierdas (Azules)
    p.setStrokeColorRGB(r1, g1, b1)
    p.line(25, height-25, 70, height-25) # Arriba izq horizontal
    p.line(25, height-25, 25, height-70) # Arriba izq vertical
    p.line(25, 25, 70, 25)               # Abajo izq horizontal
    p.line(25, 25, 25, 70)               # Abajo izq vertical

    # Esquinas Derechas (Rojas)
    p.setStrokeColorRGB(r2, g2, b2)
    p.line(width-25, height-25, width-70, height-25) # Arriba der horizontal
    p.line(width-25, height-25, width-25, height-70) # Arriba der vertical
    p.line(width-25, 25, width-70, 25)               # Abajo der horizontal
    p.line(width-25, 25, width-25, 70)               # Abajo der vertical

    # --- 2. ENCABEZADO (Izquierda) ---
    # Logo
    logo_path = os.path.join(settings.BASE_DIR, 'apps_colfrance', 'static', 'images', 'colfrance.png')
    if os.path.exists(logo_path):
        try:
            img = ImageReader(logo_path)
            p.drawImage(img, 50, height - 130, width=120, height=80, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Error al cargar logo: {e}")

    # Textos de la empresa
    p.setFillColorRGB(0.05, 0.1, 0.3) # Azul oscuro
    p.setFont("Times-Roman", 32)
    p.drawString(180, height - 85, "Alimentos Colfrance S.A.S")

    # --- 3. INFORMACIÓN DEL EMPLEADO ---
    p.setFillColorRGB(0.3, 0.3, 0.3) # Gris
    p.setFont("Helvetica", 11)
    p.drawString(180, height - 160, "SE OTORGA A")

    p.setFillColorRGB(0.04, 0.08, 0.25) # Azul muy oscuro casi negro
    p.setFont("Times-Roman", 46)
    p.drawString(180, height - 210, str(evaluacion.nombre).title())

    p.setFillColorRGB(0.2, 0.2, 0.2)
    p.setFont("Helvetica", 14)
    p.drawString(180, height - 240, f"C.C.: {evaluacion.documento}")

    # --- 4. INSIGNIAS (Pills grises de Cargo y Área) ---
    p.setLineWidth(0)
    p.setFillColorRGB(0.85, 0.85, 0.85) # Fondo gris de la insignia
    
    cargo_texto = str(evaluacion.cargo).title()
    area_texto = f"Área de {evaluacion.area}".title()
    
    p.roundRect(180, height - 280, 160, 22, 11, fill=1, stroke=0)
    p.roundRect(350, height - 280, 140, 22, 11, fill=1, stroke=0)

    # Puntos de colores en las insignias (Azul y Rojo)
    p.setFillColorRGB(r1, g1, b1)
    p.circle(192, height - 269, 3.5, fill=1, stroke=0)
    p.setFillColorRGB(r2, g2, b2)
    p.circle(362, height - 269, 3.5, fill=1, stroke=0)

    # Textos de las insignias
    p.setFillColorRGB(0.2, 0.2, 0.2)
    p.setFont("Helvetica", 10)
    p.drawString(202, height - 272, cargo_texto)
    p.drawString(372, height - 272, area_texto)

    # --- 5. LÍNEA SEPARADORA CENTRAL (Azul a Rojo) ---
    y_line = height - 315
    p.setLineWidth(2)
    p.setStrokeColorRGB(r1, g1, b1) # Lado Azul
    p.line(80, y_line, width/2, y_line)
    p.setStrokeColorRGB(r2, g2, b2) # Lado Rojo
    p.line(width/2, y_line, width-80, y_line)

    # --- 6. TÍTULO DEL CERTIFICADO ---
    p.setFillColorRGB(0.1, 0.1, 0.1)
    p.setFont("Times-Bold", 24)
    p.drawCentredString(width/2, height - 365, "CERTIFICADO DE LOGRO")

    # Nombre del Examen
    nombre_examen = dict(Evaluacion.EXAMENES).get(evaluacion.tipo_examen, evaluacion.tipo_examen).title()
    p.setFillColorRGB(0.04, 0.08, 0.25)
    p.setFont("Times-Bold", 42)
    p.drawCentredString(width/2, height - 425, nombre_examen)

    # --- 7. FIRMA Y PIE DE PÁGINA ---
    firma_path = os.path.join(settings.BASE_DIR, 'apps_colfrance', 'static', 'images', 'firma_gh.png')
    
    if os.path.exists(firma_path):
        try:
            img_firma = ImageReader(firma_path)
            p.drawImage(img_firma, width/2 - 125, 105, width=250, height=75, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Error al cargar la firma: {e}")
            p.setFillColorRGB(0.05, 0.05, 0.05)
            p.setFont("Times-BoldItalic", 42)
            p.drawCentredString(width/2, 120, "Gestión Humana")
    else:
        p.setFillColorRGB(0.05, 0.05, 0.05)
        p.setFont("Times-BoldItalic", 42)
        p.drawCentredString(width/2, 120, "Gestión Humana")

    # Línea debajo de la firma
    y_firma_line = 100
    p.setLineWidth(1.5)
    p.setStrokeColorRGB(r1, g1, b1) # Azul
    p.line(180, y_firma_line, width/2, y_firma_line)
    p.setStrokeColorRGB(r2, g2, b2) # Rojo
    p.line(width/2, y_firma_line, width-180, y_firma_line)

    p.setFillColorRGB(0.2, 0.2, 0.2)
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width/2, 82, "AUTORIZADO POR GESTIÓN HUMANA COLFRANCE S.A.")

    # Fecha en español
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    fecha_formateada = f"Expedido el {evaluacion.fecha.day} de {meses[evaluacion.fecha.month - 1]} de {evaluacion.fecha.year}"
    
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, 68, fecha_formateada)

    # Cerrar y retornar
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
    
    headers = ['Nombre', 'Documento', 'Correo', 'Área', 'Cargo', 'Examen', 'Puntaje', 'Aprobado', 'Fecha']
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
    
    area_map = dict(Evaluacion.AREAS)
    
    for d in Evaluacion.objects.all():
        nombre_area = area_map.get(d.area, d.area)
        
        ws.append([
            d.nombre, 
            d.documento, 
            d.correo, 
            nombre_area, 
            d.cargo, 
            d.tipo_examen, # Directo de la base de datos
            d.puntaje, 
            "SI" if d.aprobado else "NO", 
            d.fecha.replace(tzinfo=None)
        ])
    
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