import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import re

# Importante, crear las variables en AZURE
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "tecnologia@colfrance.com.co"
PASSWORD = "svcc bnfi obgi gxfr"


def enviar_correo( asunto, informacion):
    nombre = informacion["nombre"]
    correo = informacion["correo"]
    telefono = informacion["telefono"]
    asunto = informacion["asunto"]
    mensaje = informacion["mensaje"]
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL
        msg["To"] = correo
        msg["Subject"] = f"{asunto}"
        html = f"""
       
<!DOCTYPE html>
<html lang="es">
<body style="font-family:Arial;background:#f5f6ff;padding:20px;">
    
<div style="max-width:600px;margin:auto;background:#fff;border-radius:20px;overflow:hidden;">
    
    <div style="background:#0135e3;color:white;padding:30px;text-align:center;">
        <h1 style="margin:0;">ALIMENTOS COLFRANCE SAS</h1>
        <p>Solicitud recibida correctamente</p>
    </div>

    <div style="padding:30px;color:#333;">
        
        <p>Hola <b>{nombre}</b>,</p>

        <p>Hemos recibido tu solicitud correctamente.</p>

        <div style="background:#f5f6ff;padding:20px;border-radius:15px;">
            <p><b>📧 Correo:</b> {correo}</p>
            <p><b>📞 Teléfono:</b> {telefono}</p>
            <p><b>📝 Asunto:</b> {asunto}</p>
            <p><b>💬 Mensaje:</b><br>{mensaje}</p>
        </div>

        <p style="margin-top:25px;">
            Uno de nuestros asesores se comunicará contigo pronto.
        </p>

        <p>
            Gracias por confiar en <b style="color:#0135e3;">COLFRANCE</b>.
        </p>

        <p>
            Cordialmente,<br>
            <b>Equipo COLFRANCE</b>
        </p>
    </div>

    <div style="background:#18164b;color:white;text-align:center;padding:15px;font-size:12px;">
        © COLFRANCE · Productos lácteos colombianos
    </div>

</div>

</body>
</html>


"""

        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print(f"✅ Enviado a {correo}")

    except Exception as e:
        print(f"Error al enviar a {correo}: {e}")




