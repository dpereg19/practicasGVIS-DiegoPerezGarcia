
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
import csv

# =====================================================
# CONFIGURACIÓN
# =====================================================

ZIP_PATH = Path(
    r"C:\Users\diego\OneDrive\Escritorio\5º CURSO\1er CUATRI\PRACTICAS EMPRESA\repo\practicasGVIS-DiegoPerezGarcia\datasets\PAN13\pan13-author-profiling-test-and-training.zip"
)

OUTPUT_DIR = Path("resultados")
OUTPUT_DIR.mkdir(exist_ok=True)

# =====================================================
# 1. INSPECCIÓN DEL ZIP
# =====================================================

def inspeccionar_zip(zip_file):

    print("\n========== ESTRUCTURA DEL ZIP ==========\n")

    archivos = zip_file.infolist()

    print(f"Total de elementos: {len(archivos)}")
    print(f"Tamaño comprimido: "
          f"{sum(f.compress_size for f in archivos) / 1024**2:.2f} MB")
    print(f"Tamaño original: "
          f"{sum(f.file_size for f in archivos) / 1024**2:.2f} MB")

    print("\nPrimeros 30 elementos:\n")

    for archivo in archivos[:30]:
        print(archivo.filename)

    xml_files = [
        f for f in archivos
        if f.filename.lower().endswith(".xml")
    ]

    print(f"\nArchivos XML encontrados: {len(xml_files)}")

    return xml_files


# =====================================================
# 2. EXTRACCIÓN DE METADATOS
# =====================================================

def analizar_xml(zip_file, xml_files):

    autores = 0
    documentos = 0

    idiomas = Counter()
    edades = Counter()
    generos = Counter()

    registros = []

    errores = 0

    for archivo in xml_files:

        try:
            with zip_file.open(archivo) as f:
                tree = ET.parse(f)

            root = tree.getroot()

            # El formato PAN puede variar entre ediciones.
            # Buscamos atributos en el elemento raíz.

            atributos = {
                k.lower(): v
                for k, v in root.attrib.items()
            }

            autor_id = atributos.get("id", "No identificado")
            edad = atributos.get("age", "No especificada")
            genero = atributos.get("gender", "No especificado")
            idioma = atributos.get("lang", "No especificado")

            autores += 1

            idiomas[idioma] += 1
            edades[edad] += 1
            generos[genero] += 1

            textos = [
                element for element in root.iter()
                if element.tag.split("}")[-1].lower()
                in ("document", "text")
            ]

            num_documentos = len(textos)
            documentos += num_documentos

            registros.append({
                "archivo": archivo.filename,
                "autor_id": autor_id,
                "idioma": idioma,
                "edad": edad,
                "genero": genero,
                "documentos": num_documentos
            })

        except ET.ParseError:
            errores += 1

        except Exception as e:
            errores += 1
            print(f"Error en archivo: {archivo.filename}: {e}")

    # =================================================
    # 3. MOSTRAR RESULTADOS
    # =================================================

    print("\n========== RESULTADOS ==========\n")

    print(f"Autores/archivos XML analizados: {autores}")
    print(f"Documentos encontrados: {documentos}")
    print(f"Archivos con errores: {errores}")

    print("\nDistribución por idioma:")
    for idioma, cantidad in idiomas.items():
        print(f"  {idioma}: {cantidad}")

    print("\nDistribución por edad:")
    for edad, cantidad in edades.items():
        print(f"  {edad}: {cantidad}")

    print("\nDistribución por género:")
    for genero, cantidad in generos.items():
        print(f"  {genero}: {cantidad}")

    # =================================================
    # 4. GUARDAR RESULTADOS AGREGADOS
    # =================================================

    output_csv = OUTPUT_DIR / "pan13_metadatos.csv"

    with open(output_csv, "w", newline="", encoding="utf-8") as f:

        campos = [
            "archivo", "autor_id", "idioma",
            "edad", "genero", "documentos"
        ]

        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(registros)

    print(f"\nInforme guardado en: {output_csv}")


# =====================================================
# EJECUCIÓN
# =====================================================

def main():

    if not ZIP_PATH.exists():
        print("ERROR: No se encuentra el archivo ZIP.")
        print("Comprueba la ruta configurada en ZIP_PATH.")
        return

    with zipfile.ZipFile(ZIP_PATH, "r") as zip_file:

        xml_files = inspeccionar_zip(zip_file)

        if not xml_files:
            print("\nNo se han encontrado archivos XML.")
            print("Necesitamos inspeccionar el formato del corpus.")
            return

        analizar_xml(zip_file, xml_files)


if __name__ == "__main__":
    main()
