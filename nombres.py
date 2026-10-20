import os 

directorio_actual = os.path.dirname(os.path.abspath(__file__))

lista1="alumnos.txt"

lista2=[]

try:
    with open(lista1, "r", encoding="utf-8") as archivo:
        lista2 = [linea.strip().replace(" ", "").lower() for linea in archivo]
except FileNotFoundError:
    print(f"No se encontró '{lista1}' en la carpeta de ejecución.")


nombre_archivo = "alumnos2.txt"

with open(nombre_archivo, "w", encoding="utf-8") as archivo:
    for linea in lista2:
        archivo.writelines(f"{linea}\n")