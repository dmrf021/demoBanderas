import os
import requests

# Carpeta donde se guardarán las banderas
CARPETA = r"C:\Users\david\proyectoBanderas\assets\banderas"
os.makedirs(CARPETA, exist_ok=True)

# Lista de países de Europa y sus códigos ISO (según flagpedia)
# Puedes agregar o quitar países si quieres
paises_europa = {
    "al": "Albania",
    "ad": "Andorra",
    "am": "Armenia",
    "at": "Austria",
    "by": "Bielorrusia",
    "be": "Bélgica",
    "ba": "Bosnia y Herzegovina",
    "bg": "Bulgaria",
    "hr": "Croacia",
    "cy": "Chipre",
    "cz": "Chequia",
    "dk": "Dinamarca",
    "ee": "Estonia",
    "fi": "Finlandia",
    "fr": "Francia",
    "ge": "Georgia",
    "de": "Alemania",
    "gr": "Grecia",
    "hu": "Hungría",
    "is": "Islandia",
    "ie": "Irlanda",
    "it": "Italia",
    "kz": "Kazajistán",
    "xk": "Kosovo",
    "lv": "Letonia",
    "li": "Liechtenstein",
    "lt": "Lituania",
    "lu": "Luxemburgo",
    "mt": "Malta",
    "md": "Moldavia",
    "mc": "Mónaco",
    "me": "Montenegro",
    "nl": "Países Bajos",
    "mk": "Macedonia del Norte",
    "no": "Noruega",
    "pl": "Polonia",
    "pt": "Portugal",
    "ro": "Rumanía",
    "ru": "Rusia",
    "sm": "San Marino",
    "rs": "Serbia",
    "sk": "Eslovaquia",
    "si": "Eslovenia",
    "es": "España",
    "se": "Suecia",
    "ch": "Suiza",
    "tr": "Turquía",
    "ua": "Ucrania",
    "gb": "Reino Unido",
    "va": "Ciudad del Vaticano"
}

# URL base de flagpedia
URL_BASE = "https://flagcdn.com/{code}.svg"

print(f"Descargando {len(paises_europa)} banderas...")

for codigo, nombre in paises_europa.items():
    url = URL_BASE.format(code=codigo)
    archivo = os.path.join(CARPETA, f"{nombre.replace(' ', '_')}.svg")

    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(archivo, "wb") as f:
                f.write(r.content)
            print(f"✅ {nombre} descargada correctamente.")
        else:
            print(f"No se pudo descargar {nombre} (HTTP {r.status_code}).")
    except Exception as e:
        print(f"Error con {nombre}: {e}")

print("\nDescarga completa.")
