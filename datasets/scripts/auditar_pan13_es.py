
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from collections import Counter
import csv
import statistics

PAQUETES_DIR = (
    Path.cwd() / "PAN13" / "paquetes_internos"
    if (Path.cwd() / "PAN13" / "paquetes_internos").exists()
    else Path.cwd() / "datasets" / "PAN13" / "paquetes_internos"
)

ZIP_PATH = PAQUETES_DIR / (
    "pan13-author-profiling-training-corpus-2013-01-09.zip"
)

resultados = []
errores = []

with ZipFile(ZIP_PATH, "r") as z:
    archivos = [
        n for n in z.namelist()
        if n.lower().endswith(".xml")
        and "/es/" in n.replace("\\", "/")
    ]

    print(f"XML españoles encontrados: {len(archivos)}")

    for i, nombre in enumerate(archivos, start=1):
        try:
            root = ET.fromstring(z.read(nombre))

            conversaciones = root.find("conversations")
            elementos = (
                list(conversaciones)
                if conversaciones is not None
                else []
            )

            longitudes = [
                len(c.text or "")
                for c in elementos
            ]

            resultados.append({
                "archivo": Path(nombre).name,
                "idioma": root.get("lang"),
                "edad": root.get("age_group"),
                "genero": root.get("gender"),
                "num_conversaciones": len(elementos),
                "caracteres_total": sum(longitudes),
            })

        except Exception as e:
            errores.append((nombre, str(e)))

        if i % 1000 == 0:
            print(f"Procesados: {i}/{len(archivos)}")

# Resúmenes
print("\n========== AUDITORÍA PAN13 ESPAÑOL ==========")
print("Autores procesados:", len(resultados))
print("Errores:", len(errores))

print("\nDistribución por edad:")
print(Counter(r["edad"] for r in resultados))

print("\nDistribución por género:")
print(Counter(r["genero"] for r in resultados))

print("\nDistribución por número de conversaciones:")
print(Counter(r["num_conversaciones"] for r in resultados).most_common(15))

longitudes = [r["caracteres_total"] for r in resultados]

if longitudes:
    print("\nLongitud total de texto por autor:")
    print("Media:", round(statistics.mean(longitudes), 2))
    print("Mediana:", statistics.median(longitudes))
    print("Mínimo:", min(longitudes))
    print("Máximo:", max(longitudes))

# Guardar únicamente metadatos agregables por autor, sin textos.
salida = PAQUETES_DIR.parent / "auditoria_pan13_es.csv"

with open(salida, "w", newline="", encoding="utf-8") as f:
    campos = [
        "archivo", "idioma", "edad", "genero",
        "num_conversaciones", "caracteres_total"
    ]
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(resultados)

print("\nCSV de auditoría guardado en:", salida)
