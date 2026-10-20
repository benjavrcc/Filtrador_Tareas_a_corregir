# Instrucciones de uso para filtrar tareas

##  Requisitos previos

Antes de empezar, asegúrate de:

1. Copiar del excel de asignaciones, los nombres de los estudiantes cuyas tareas te corresponden revisar y pegalos en el archivo vacío "alumnos.txt"
2. Descarga el archivo de tareas del buzón y nombralo como "submissions_T{numero}.zip" donde {numero} es el número de la tarea.
3. Asegurate de tener todos los códigos y archivos (.txt y .zip) en la misma carpeta tal como están ordenados en el repositorio.
4. Recomiendo descargar el zip del buzón oficial y nombrarlo "submissions_T{numero}.zip", luego de correr el código, obtendras los nombres de los estudiantes no encontrados, usualmente son pocos y puedes encontrarlos más facil a mano en el buzón de rezagados.

##  Ejecución

Sigue estos pasos para obtener el zip solo con las tareas que tienes que revisar.

1. Corre el código nombres.py para obtener el archivo "alumnos2.txt"
   
2. Corre el código encontrar_tildes.py para asegurarte de que los nombres que vas a buscar no tienen tilde, si alguno viene con un tilde, debes quitarselo editando manualmente "alumnos2.txt".

3. Corre el código main.py, te va a preguntar en la consola el numero de tarea, debes ingresarlo y vas a obtener el zip solo con las tareas que tienes que revisar y el reporte de los estudiantes cuyas tareas no fueron encontradas. 

4. Si quieres saber un poco más, revisa abajo una explicación breve de cada código, recomiendo no cambiar los nombres de los archivos que produce cada uno de los códigos y nombrar los archivos como digo en estas instrucciones, ya que todos los nombres de archivos están asociados a algo en el código.

## Códigos presentes

* **nombres.py:** Este codigo abre un archivo llamado "alumnos.txt" que contiene en sus lineas los nombres completos de los alumnos tal como si los copiaramos del excel y los pegaramos en un txt. Luego de recorrer este archivo, nos entrega otro archivo llamado "alumnos2.txt" que tiene exactamente la misma cantidad de lineas que alumnos.txt y los mismos nombres pero en minuscula y sin espacio entre palabras, esto con el objetivo de encontrar las tareas en el zip de submissions

* **encontrar_tildes.py:** Este código toma un archivo de tipo txt llamado "alumnos2.txt" y lo recorre para asegurar que ningun nombre tenga tilde, ya que en el zip de submissions vienen con tilde pero en el excel de asignaciones no, esto es solo para asegurar que los nombres que vienen no tienen tilde, de todas formas, el siguiente código se encarga de hacer el matching entre los nombres de la lista y de los archivos de tareas independiente de si estos tienen tilde o no.


* **main.py:** Toma ambos archivos txt con nombres y el zip de submissions, con esto, busca las tareas de los estudiantes en la lista en el zip que contiene todas las tareas. Genera una carpeta comprimida en zip llamada "corregir_T{numero}.zip" solamente con las tareas que te corresponden revisar del buzón que estás analizando (puede ser el oficial o el de rezagados), además entrega un txt llamado "Reporte_Tarea{numero}.txt" que indica cuantas tareas fueron encontradas correctamente, cuantas NO fueron encontradas y los nombres de los estudiantes cuyas tareas no fueron encontradas



