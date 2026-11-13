# Protocolo de pruebas

Pruebas **manuales**. Cada fila es un caso. Ejecutar sobre el tag que entregan.

Leyenda de resultado: `pasa` / `no pasa` / `no corrido`.

Mínimos: 8 casos escritos en E2; ejecutados en E3; 15 de regresión en E6 (pila, cola, archivos, recursión, búsquedas).

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | E1 | Arrancar el programa y listar catálogo | dataset de la cátedra | lista no vacía, sin traceback | pasa | El catálogo se lista correctamente. |
| P02 | E1 | Elegir un ítem inexistente en la opción Ver detalle | id = -1 | mensaje claro, el menú sigue | pasa | Se informa que el ítem no existe y el menú continúa. |
| P03 | E2 | Operación recursiva sobre un ítem con cadena | ID = 1 | imprime la cadena completa | pasa | Muestra la cadena de versiones 2, 3 y 4. |
| P04 | E2 | Operación recursiva sobre un ítem sin derivados | ID = 4 | solo el ítem (caso base) | pasa | El ítem no tiene derivados. |
| P05 | E3 | Agregar a la colección principal hasta el tope | equipo de 6 / equivalente | el séptimo falla con excepción propia | pasa | |
| P06 | E3 | Desapilar historial vacío | pila vacía | excepción propia, menú sigue | pasa | |
| P07 | E3 | Desencolar cola vacía | cola vacía | excepción propia, menú sigue | pasa | |
| P08 | E3 | Listar colección con el iterador | 2+ ítems | el orden coincide con las inserciones | pasa | |
| P09 | E4 | Búsqueda lineal de un nombre que existe | Canción del catálogo | lo encuentra y lo muestra | pasa | Búsqueda por título correcta. |
| P10 | E4 | Búsqueda lineal de un nombre que no existe | Título inexistente | "no encontrado", sin traceback, el menú sigue | pasa | Manejo de excepción/búsqueda nula. |
| P11 | E4 | Búsqueda binaria con el catálogo desordenado | Canción desordenada | avisa o reordena; no da un falso "no encontrado" | pasa | Reordena automáticamente y busca. |
| P12 | E4 | Ordenar por un criterio y después por otro | Título y Año/Duración | el orden cambia correctamente | pasa | Selección e inserción funcionales. |
| P13 | E5 | Guardar TXT, salir, volver a entrar y cargar el archivo | catálogo de 5 canciones | los datos se conservan al cargar el archivo | pasa | Se guardó y cargó el TXT correctamente. |
| P14 | E5 | Guardar binario y modificar un registro por ID | catálogo de 5 canciones | al recargar, ese campo cambió | pasa | Modificación del registro persistida correctamente. |
| P15 | E5 | Abrir un binario truncado o con magia mala | archivo inválido | excepción de archivo inválido | pasa | Se detecta el archivo inválido y se informa mediante la excepción correspondiente. |