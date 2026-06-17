import base64
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from pathlib import Path

RUTA_ACTUAL = Path(__file__).resolve()
RUTA_PADRE = RUTA_ACTUAL.parent
PATH_TEMPLATES_WEB = "tecnologia/views/"


def generar_acta_con_firma(request):
    # Si la petición es POST, procesamos la firma y generamos el PDF
    if request.method == "POST":
        firma_b64 = request.POST.get("firma_base64")

        # Validar que realmente se envió una firma
        if not firma_b64:
            return HttpResponse("Error: No se proporcionó la firma.", status=400)

        # Limpiar la cadena base64 (remover el "data:image/png;base64,")
        try:
            formato, imgstr = firma_b64.split(";base64,")
            firma_bytes = base64.b64decode(imgstr)
            # Pillow leerá estos bytes como una imagen válida
            firma_imagen = ImageReader(BytesIO(firma_bytes))
        except Exception as e:
            return HttpResponse(f"Error al procesar la imagen: {str(e)}", status=400)

        # Crear la respuesta HTTP configurada como PDF
        response = HttpResponse(content_type="application/pdf")
        # Si quieres que se descargue, usa 'attachment'. Para ver en el navegador, usa 'inline'.
        response["Content-Disposition"] = 'inline; filename="acta_generada.pdf"'

        # Iniciar el lienzo de ReportLab
        p = canvas.Canvas(response, pagesize=letter)
        ancho_pagina, alto_pagina = letter

        # --- GENERACIÓN DEL ACTA ---
        # Título
        p.setFont("Helvetica-Bold", 16)
        p.drawCentredString(
            ancho_pagina / 2, alto_pagina - 100, "ACTA DE ENTREGA / REUNIÓN"
        )

        # Cuerpo del texto
        p.setFont("Helvetica", 12)
        texto_acta = (
            "En la ciudad de Bogotá, se reúnen las partes interesadas para dejar "
            "constancia de la revisión y aceptación de los términos estipulados "
            "en el presente documento. El usuario confirma su conformidad mediante "
            "la firma electrónica plasmada a continuación."
        )

        # Para textos largos, es mejor usar un objeto de texto (TextObject)
        text_object = p.beginText(50, alto_pagina - 160)
        text_object.setFont("Helvetica", 12)
        text_object.setLeading(14)

        # Simulación de salto de línea básico para el ejemplo
        lineas = texto_acta.split(". ")
        for linea in lineas:
            text_object.textLine(linea + ".")
        p.drawText(text_object)

        # --- INCRUSTAR LA FIRMA ---
        p.drawString(50, 200, "________________________________")
        p.drawString(50, 185, "Firma de Aceptación")

        # Dibujar la imagen (coordenada X, coordenada Y, ancho, alto)
        # La máscara 'auto' preserva la transparencia del PNG
        p.drawImage(firma_imagen, 50, 210, width=200, height=100, mask="auto")

        # Finalizar y guardar el PDF
        p.showPage()
        p.save()

        return response

    # Si la petición es GET, simplemente mostramos el HTML
    return render(request, f"{PATH_TEMPLATES_WEB}acta_firma.html")
