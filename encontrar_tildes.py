
lista1="alumnos2.txt"

with open(lista1, "r", encoding="utf-8") as archivo:
    tildes = ["á", "é", "í", "ó", "ú"]
    lista2 = [linea.strip() for linea in archivo]
    i=0
    for nombre in lista2:
        k = len(nombre)
        j = 0
        for char in nombre:
            if char in tildes:
                print(f"tilde encontrada en {nombre}")
                j+=1
        if j>=0:
            i+=1  
            print(f"nombre {i} sin tilde")
    