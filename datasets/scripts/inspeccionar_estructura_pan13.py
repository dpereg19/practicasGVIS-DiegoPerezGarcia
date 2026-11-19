
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from collections import Counter

PAQUETES_DIR = (
    Path.cwd() / "PAN13" / "paquetes_internos"
    if (Path.cwd() / "PAN13" / "paquetes_internos").exists()
    else Path.cwd() / "datasets" / "PAN13" / "paquetes_internos"
)

zip_training = PAQUETES_DIR / (
    "pan13-author-profiling-training-corpus-2013-01-09.zip"
)

with ZipFile(zip_training, "r") as z:
    nombre = next(
        n for n in z.namelist()
        if n.endswith(".xml") and "/es/" in n.replace("\\", "/")
    )

    root = ET.fromstring(z.read(nombre))

    print("ARCHIVO:", nombre)
    print("\nESTRUCTURA DEL XML")
    print("(No se muestra el texto de las publicaciones)\n")

    def inspeccionar(elemento, nivel=0):
        sangria = "  " * nivel

        # Mostramos nombres de atributos, no sus valores.
        atributos = list(elemento.attrib.keys())

        # Longitud del texto, sin mostrar su contenido.
        longitud_texto = len(elemento.text or "")

        print(
            f"{sangria}- {elemento.tag} "
            f"| atributos: {atributos} "
            f"| hijos: {len(elemento)} "
            f"| longitud_texto: {longitud_texto}"
        )

        for hijo in elemento:
            inspeccionar(hijo, nivel + 1)

    inspeccionar(root)

    print("\nRESUMEN DE ETIQUETAS")
    contador = Counter(elemento.tag for elemento in root.iter())

    for etiqueta, cantidad in contador.most_common():
        print(f"{etiqueta}: {cantidad}")
