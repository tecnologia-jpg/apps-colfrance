import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import re


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "tecnologia@colfrance.com.co"
PASSWORD = "svcc bnfi obgi gxfr"

ruta = r"C:\Users\nocua\Downloads\usuariosarco.xlsx"


def leer_archivo(ruta):
    df = pd.read_excel(ruta)
    print(df)
    return df


def enviar_correo(usuario, nombre, correo, contraseña):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL
        msg["To"] = correo
        msg["Subject"] = f"IMPLEMENTACION ARCO 2026 - Usuario de arco para {nombre}"

        html = f""""
        <!-- Asunto: IMPLEMENTACION ARCO 2026 - Usuario de arco para {nombre} -->

         <html>
    <body style="font-family: Arial, sans-serif; background-color:#f4f6f9; padding:20px;">
    
    <div style="max-width:600px; margin:auto; background:#ffffff; padding:25px; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
      
      <h2 style="color:#2c3e50; text-align:center;">
        Implementación ARCO 2026
      </h2>

      <p style="font-size:15px; color:#555;">
        Estimado(a) <strong>{nombre}</strong>,
      </p>

      <p style="font-size:15px; color:#555;">
        Desde el área de <strong>Tecnología - Colfrance</strong>, informamos que ha sido creado y asignado su usuario en el sistema <strong>ARCO</strong>.
      </p>

      <p style="font-size:15px; color:#555;">
        A continuación, encontrará sus credenciales de acceso:
      </p>

      <div style="background:#f1f3f6; padding:15px; border-radius:8px; margin:20px 0;">
        <p style="margin:5px 0;"><strong>Nombre:</strong> {nombre}</p>
        <p style="margin:5px 0;"><strong>Correo:</strong> {correo}</p>
        <p style="margin:5px 0;"><strong>Usuario:</strong> {usuario}</p>
        <p style="margin:5px 0;"><strong>Contraseña:</strong> {contraseña}</p>
      </div>

      <p style="font-size:14px; color:#777;">
        Por motivos de seguridad, le recomendamos cambiar su contraseña al ingresar por primera vez al sistema.
      </p>

      <div style="text-align:center; margin-top:20px;">
        <a href="https://colfrance_qas.arco365.com/"
           style="background:#3498db; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; font-size:14px;">
           Acceder al sistema ARCO
        </a>
      </div>

      <hr style="margin:25px 0;">

      <p style="font-size:12px; color:#999; text-align:center;">
        Este es un mensaje automático generado por el área de Tecnología de Colfrance.
      </p>

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


data = leer_archivo(ruta)


def procesar_info(data):
   
    for index, fila in data.iterrows():
        correo = fila["CORREO"]

        # filtra: vacíos, NaN, tu propio correo y formatos inválidos
        if (
            pd.isna(correo)
            or not isinstance(correo, str)
            or correo.strip() == ""
            or correo.strip().lower() == "tecnologia@colfrance.com.co"
            or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo.strip())
        ):
            continue

        print(fila["NOMBRE"], fila["RESPONSABLE"], correo.strip(), fila["CONTRASEÑA"])
        enviar_correo(
            fila["NOMBRE"], fila["RESPONSABLE"], correo.strip(), fila["CONTRASEÑA"]
        )
        
        # enviar_correo("admin", "Alex Nocua", "tecnologia@colfrance.com.co", "1234")


procesar_info(data)
