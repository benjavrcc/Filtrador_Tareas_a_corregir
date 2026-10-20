from pathlib import Path
from typing import Iterable
import unicodedata
import zipfile


def quitar_tildes(texto: str) -> str:
    return "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def encontrar_nombre(nombre: str, txt_nombres_completos_path: str) -> str:
    path_txt = Path(txt_nombres_completos_path)
    with open(path_txt, mode="r", encoding="utf-8") as f:
        nombres_objetivo = [linea.strip() for linea in f if linea.strip()]
        for name in nombres_objetivo:
            if name.strip().replace(" ", "").lower() == nombre:
                return name
    return nombre


def generar_reporte_txt(
    ruta_txt_salida: str,
    lista1: Iterable[str],
    n: int,
    txt_nombres_completos_path: str,
    titulo: str = "REPORTE DE ARCHIVOS PROCESADOS",
    nota_inicial: str = "La cantidad de tareas de tu sección encontradas exitosamente dentro del zip fueron",
    nota_final: str = "Para estos estudiantes, se recomienda revisar a mano si es que existió una diferencia en el nombre de la tarea, si entregará en el buzón de rezagados, si convalidó la nota del laboratorio o si simplemente hay que chantarle el 1",
) -> None:
    path_txt = Path(ruta_txt_salida)

    # 1. Validación: asegurar que no exista previamente
    if path_txt.exists():
        raise FileExistsError(
            f"El archivo '{path_txt.name}' ya existe en la ruta de destino."
        )

    tareas_no_encontradas = len(lista1)
    lista2 = set()
    for elem in lista1:
        lista2.add(encontrar_nombre(elem, txt_nombres_completos_path))

    # 2. Construcción y escritura del archivo
    with open(path_txt, mode="w", encoding="utf-8") as f:
        f.write(f"====================== {titulo} ======================\n\n")
        f.write(f"========================================================\n\n")
        f.write(
            f"Este es un reporte que indica el exito en la recopilación de tareas de la sección 18 correspondiente a la tarea {str(n)} \n\n"
        )

        if nota_inicial:
            f.write(f"{nota_inicial}\n\n")
        f.write(
            f"{str(89 - tareas_no_encontradas)} de un total de 89 alumnos en la sección\n\n"
        )
        f.write(
            f"A continuación, se muestran los nombres de los estudiantes cuyas tareas no se encontraron\n\n"
        )

        f.write("Nombres:\n")
        total = 0
        for nombre in lista2:
            f.write(f"- {nombre}\n")
            total += 1
        f.write(f"========================================================\n\n")
        f.write(f"Total contabilizado de tareas sin encontrar: {total}\n")
        f.write(f"========================================================\n\n")

        if nota_final:
            f.write(f"{nota_final}\n")


def filtrar_zip_por_lista(
    zip_origen_path: str, txt_nombres_path: str, zip_destino_path: str
) -> set[str]:
    path_zip_in = Path(zip_origen_path)
    path_txt = Path(txt_nombres_path)
    path_zip_out = Path(zip_destino_path)

    # 1. Validaciones previas de existencia
    if not path_zip_in.is_file():
        raise FileNotFoundError(
            f"El archivo ZIP de origen no existe: {path_zip_in}"
        )

    if not path_txt.is_file():
        raise FileNotFoundError(
            f"El archivo TXT de nombres no existe: {path_txt}"
        )

    if path_zip_out.exists():
        raise FileExistsError(
            f"El ZIP de destino ya existe para evitar sobreescritura accidental: {path_zip_out}"
        )

    # 2. Cargar y limpiar la lista de nombres del TXT
    with open(path_txt, mode="r", encoding="utf-8") as f:
        nombres_objetivo = {
            linea.strip() for linea in f if linea.strip()
        }

    # 3. Procesar el ZIP origen y escribir en el nuevo ZIP
    try:
        with zipfile.ZipFile(
            path_zip_in, "r"
        ) as z_in, zipfile.ZipFile(
            path_zip_out, "w", compression=zipfile.ZIP_DEFLATED
        ) as z_out:

            nombres_encontrados = set()

            for item in z_in.infolist():
                if item.is_dir():
                    continue

                nombre_archivo = Path(item.filename).name

                if (
                    nombre_archivo.endswith(".nb")
                    and "_" in nombre_archivo
                ):
                    prefijo1 = nombre_archivo.split("_", 1)[0]
                    prefijo = quitar_tildes(prefijo1)

                    if prefijo in nombres_objetivo:
                        nombres_encontrados.add(prefijo)
                        data = z_in.read(item.filename)
                        z_out.writestr(nombre_archivo, data)

            no_encontrados = list(nombres_objetivo - nombres_encontrados)
            return no_encontrados

    except zipfile.BadZipFile:
        if path_zip_out.exists():
            path_zip_out.unlink()
        raise zipfile.BadZipFile(
            f"El archivo ZIP está dañado o corrupto: {path_zip_in}"
        )

    except Exception as e:
        if path_zip_out.exists():
            path_zip_out.unlink()
        raise e


# --- Bloque principal corregido ---
if __name__ == "__main__":
    try:
        numero_tarea = int(input("Ingresar el numero de la tarea: "))
        zip_destino_path = f"corregir_T{str(numero_tarea)}.zip"
        txt_nombres_path = "alumnos2.txt"
        zip_origen_path = f"submissions_T{str(numero_tarea)}.zip"
        ruta_salida = f"Reporte_Tarea{str(numero_tarea)}.txt"

        # Manejo de archivos de salida previos para que tus funciones no tiren FileExistsError
        salida_zip = Path(zip_destino_path)
        if salida_zip.exists():
            print(
                f"Aviso: El archivo '{zip_destino_path}' ya existía. Eliminando versión previa..."
            )
            salida_zip.unlink()

        salida_reporte = Path(ruta_salida)
        if salida_reporte.exists():
            print(
                f"Aviso: El archivo '{ruta_salida}' ya existía. Eliminando versión previa..."
            )
            salida_reporte.unlink()

        # 1. Llamar a la función UNA VEZ y capturar los no encontrados
        print(f"Procesando '{zip_origen_path}'...")
        tareas_faltantes = filtrar_zip_por_lista(
            zip_origen_path=zip_origen_path,
            txt_nombres_path=txt_nombres_path,
            zip_destino_path=zip_destino_path,
        )

        # 2. Pasar el resultado a la generación del reporte
        generar_reporte_txt(
            ruta_txt_salida=ruta_salida,
            lista1=tareas_faltantes,
            n=numero_tarea,
            txt_nombres_completos_path="alumnos.txt",
            titulo="REPORTE DE ARCHIVOS PROCESADOS",
            nota_inicial="La cantidad de tareas de tu sección encontradas exitosamente dentro del zip fueron",
            nota_final="Para estos estudiantes, se recomienda revisar a mano si es que existió una diferencia en el nombre de la tarea, si entregará en el buzón de rezagados, si convalidó la nota del laboratorio o si simplemente hay que chantarle el 1",
        )

        print(f"Proceso finalizado con éxito.")
        print(f"- ZIP generado: {zip_destino_path}")
        print(f"- Reporte generado: {ruta_salida}")

    except ValueError as e:
        print("Error: El número de la tarea ingresado debe ser un número entero.")
    except FileNotFoundError as e:
        print(f"Error de archivo no encontrado: {e}")
    except FileExistsError as e:
        print(f"Error de archivo existente: {e}")
    except zipfile.BadZipFile as e:
        print(f"Error con el archivo comprimido: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la ejecución: {e}")