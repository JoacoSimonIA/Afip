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
novedades = data["d"]["data"]

# 4️⃣ Armamos el bloque de texto
bloque = "Titulos\n\n"

for i, item in enumerate(novedades, start=1):
    bloque += f"{i}: {item['Titulo']}\n"

# 5️⃣ Guardamos en un archivo .txt
with open("titulos_afip.txt", "w", encoding="utf-8") as f:
    f.write(bloque)

print("Archivo creado correctamente: titulos_afip.txt")