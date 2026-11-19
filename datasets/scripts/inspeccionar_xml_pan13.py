
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

# Localizar la carpeta de los ZIP internos.
candidatos = [
    Path.cwd() / "PAN13" / "paquetes_internos",
    Path.cwd() / "datasets" / "PAN13" / "paquetes_internos",
]

PAQUETES_DIR = next(
    (p for p in candidatos if p.exists()),
    None
)

if PAQUETES_DIR is None:
    raise FileNotFoundError(
        "No se encuentra la carpeta paquetes_internos. "
        "Comprueba la ruta."
    )

zip_training = PAQUETES_DIR / (
    "pan13-author-profiling-training-corpus-2013-01-09.zip"
)

if not zip_training.exists():
    raise FileNotFoundError(f"No se encuentra: {zip_training}")

with ZipFile(zip_training, "r") as z:
    xml_files = [
        name for name in z.namelist()
        if name.lower().endswith(".xml")
    ]

    # Elegimos un XML del corpus español.
    ejemplos = [
        name for name in xml_files
        if "/es/" in name.replace("\\", "/")
    ]

    if not ejemplos:
        ejemplos = xml_files

    if not ejemplos:
        raise RuntimeError("No se han encontrado XML.")

    nombre = ejemplos[0]
    contenido = z.read(nombre)

    root = ET.fromstring(contenido)

    print("========== EJEMPLO XML PAN13 ==========")
    print("Archivo:", nombre)
    print("Etiqueta raíz:", root.tag)
    print("Atributos de la raíz:", root.attrib)

    print("\nHijos directos de la raíz:")
    for child in root:
        print(
            "Etiqueta:", child.tag,
            "| Atributos:", child.attrib,
            "| Número de hijos:", len(child)
        )

    print("\nPrimeros elementos de la estructura:")
    for element in root.iter():
        print(
            "Etiqueta:", element.tag,
            "| Atributos:", element.attrib
        )
        if element is not root and len(list(root.iter())) > 30:
            # Limitar la salida para no imprimir demasiado.
            pass
        # Solo mostramos una muestra de la estructura.
        if element is list(root.iter())[-1]:
            break
