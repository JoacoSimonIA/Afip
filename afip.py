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

# 4️⃣ Armamos el bloque de texto
bloque = "Titulos\n\n"

for i, item in enumerate(novedades, start=1):
    bloque += f"{i}: {item['Titulo']}\n"

# 5️⃣ Guardamos en un archivo .txt
with open("titulos_afip.txt", "w", encoding="utf-8") as f:
    f.write(bloque)


print("Archivo creado correctamente: titulos_afip.txt")

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


