#!/bin/bash

echo "Iniciando el script de despliegue personalizado..."

# 1. Ejecutar las migraciones de la base de datos
echo "Aplicando migraciones de Django..."
python manage.py migrate

# (Opcional) Recopilar archivos estáticos. 
# Si tu app usa el panel de administración de Django o sirve CSS/JS propios, descomenta la siguiente línea:
# echo "Recolectando archivos estáticos..."
# python manage.py collectstatic --noinput

# 2. Iniciar la aplicación con el comando que me proporcionaste
echo "Iniciando Gunicorn..."
gunicorn apps_colfrance.wsgi --bind=0.0.0.0:8000