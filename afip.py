import requests

# Endpoint
url = "https://servicioscf.afip.gob.ar/publico/sitio/contenido/novedad/listado.aspx/ListarNovedades"

headers = {
    "Content-Type": "application/json; charset=UTF-8"
}

# 1️⃣ Hacemos el POST
response = requests.post(url, headers=headers, json={})

# 2️⃣ Convertimos la respuesta a JSON
data = response.json()

# 3️⃣ Entramos a ["d"]["data"]
novedades = data["d"]["data"][:30]

# Leer titulos previos
try:
    with open("titulos_previos.txt", "r", encoding="utf-8") as f:
        titulos_previos = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    titulos_previos = []

# 4️⃣ Armamos el bloque de texto
titulos_actuales = []

for novedad in novedades:
    titulo = novedad["Titulo"]
    titulos_actuales.append(titulo)

titulos_nuevos = []

for titulo in titulos_actuales:
    if titulo not in titulos_previos:
        titulos_nuevos.append(titulo)

if not titulos_nuevos:
    print("No hay titulos nuevos")
    exit()

# 5️⃣ Guardamos en un archivo .txt

archivo = "titulos_afip.txt"

with open(archivo, "w", encoding="utf-8") as f:
    f.write("Titulos nuevos AFIP\n\n")

    for titulo in titulos_nuevos:
        f.write(titulo + "\n\n")

print("Archivo creado correctamente:", archivo)

with open("titulos_previos.txt", "w", encoding="utf-8") as f:
    for titulo in titulos_actuales:
        f.write(titulo + "\n")

import os
import smtplib
from email.message import EmailMessage

# Datos desde GitHub Secrets
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_TO = os.environ["EMAIL_TO"]

# Crear mensaje
msg = EmailMessage()
msg["Subject"] = "Archivo AFIP automático"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO
msg.set_content("Adjunto el archivo generado automáticamente.")

# Adjuntar el archivo (cambiá el nombre si tu archivo se llama distinto)
archivo = "titulos_afip.txt"

with open(archivo, "rb") as f:
    file_data = f.read()
    file_name = f.name

msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

# Enviar mail
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_USER, EMAIL_PASS)
    smtp.send_message(msg)

print("Mail enviado correctamente.")





