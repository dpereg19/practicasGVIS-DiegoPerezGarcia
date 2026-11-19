
import zipfile
from pathlib import Path
from collections import Counter

# =====================================================
# CONFIGURACIÓN
# =====================================================

BASE_DIR = Path(
    r"C:\Users\diego\OneDrive\Escritorio\5º CURSO\1er CUATRI\PRACTICAS EMPRESA\repo\practicasGVIS-DiegoPerezGarcia"
)

ZIP_PATH = BASE_DIR / "datasets" / "PAN13" / "pan13-author-profiling-test-and-training.zip"

OUTPUT_DIR = BASE_DIR / "datasets" / "PAN13" / "paquetes_internos"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# 1. LOCALIZAR ZIP INTERIORES
# =====================================================

def localizar_zip_interiores():

    with zipfile.ZipFile(ZIP_PATH, "r") as outer_zip:

        archivos = [
            info for info in outer_zip.infolist()
            if info.filename.lower().endswith(".zip")
        ]

        print("\n========== ZIP INTERIORES ==========\n")

        for archivo in archivos:
            print(f"Nombre: {archivo.filename}")
            print(f"Tamaño: {archivo.file_size / 1024**2:.2f} MB")
            print()

        return archivos


# =====================================================
# 2. EXTRAER LOS ZIP INTERIORES
# =====================================================

def extraer_zip_interiores(archivos):

    with zipfile.ZipFile(ZIP_PATH, "r") as outer_zip:

        for archivo in archivos:

            nombre = Path(archivo.filename).name
            destino = OUTPUT_DIR / nombre

            if destino.exists():
                print(f"Ya existe: {nombre}")
                continue

            print(f"Extrayendo: {nombre}")

            with outer_zip.open(archivo) as origen:
                with open(destino, "wb") as salida:

                    while True:
                        bloque = origen.read(1024 * 1024)

                        if not bloque:
                            break

                        salida.write(bloque)

            print("Extracción completada.\n")


# =====================================================
# 3. INSPECCIONAR CONTENIDO
# =====================================================

def inspeccionar_contenido():

    for zip_path in sorted(OUTPUT_DIR.glob("*.zip")):

        print("\n========================================")
        print(f"ARCHIVO: {zip_path.name}")
        print("========================================")

        with zipfile.ZipFile(zip_path, "r") as inner_zip:

            archivos = inner_zip.infolist()

            print(f"\nTotal de elementos: {len(archivos)}")

            print(
                f"Tamaño original: "
                f"{sum(f.file_size for f in archivos) / 1024**2:.2f} MB"
            )

            extensiones = Counter(
                Path(f.filename).suffix.lower()
                for f in archivos
                if not f.is_dir()
            )

            print("\nDistribución por extensión:")

            for extension, cantidad in extensiones.most_common():
                print(f"{extension or '[sin extensión]'}: {cantidad}")

            print("\nPrimeros 30 archivos:")

            for archivo in archivos[:30]:
                print(archivo.filename)


# =====================================================
# EJECUCIÓN
# =====================================================

def main():

    if not ZIP_PATH.exists():
        print(f"ERROR: No se encuentra el archivo: {ZIP_PATH}")
        return

    archivos = localizar_zip_interiores()

    extraer_zip_interiores(archivos)

    inspeccionar_contenido()


if __name__ == "__main__":
    main()
