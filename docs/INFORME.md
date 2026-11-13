# Informe del TP

Completar y hacer crecer en cada entrega. No hace falta prosa larga: oraciones claras y tablas.

## 1. Grupo y tema

- Tema: Biblioteca musical (canciones)
- Por qué lo eligieron (5–8 líneas):
Elegimos la biblioteca musical porque es un dominio cotidiano y muy visual para organizar datos. Nos pareció muy claro cómo asociar cada estructura de la materia con un reproductor de música. 
Por ejemplo, una playlist se adapta perfecto a una lista, el historial de reproducción a una pila,
y la cola de temas a una cola. Además, manejar atributos como artista, género y duración nos permite hacer búsquedas y ordenamientos interesantes más adelante. Resulta un tema muy intuitivo para trabajar.

## 2. Modelo

Qué es un ítem del catálogo. Qué es mutable y qué no (E1). Cómo se relacionan catálogo, colección principal, pila y cola.

- **Ítem del catálogo (`Cancion`):** Representa una pista musical individual.
  - **Atributos inmutables:** `id` (`str`), `titulo` (`str`), `artista` (`str`), `album` (`str`) y `genero` (`str`) son cadenas de texto; `anio` (`int`) y `duracion_seg` (`int`) son enteros. Son tipos inmutables en Python para asegurar la consistencia de los datos básicos de la canción.
- **Catálogo (`list`):** Es una estructura **mutable** que agrupa los objetos de tipo `Cancion`. Se eligió una lista mutable para permitir futuras modificaciones, busquedas y ordenamientos sobre el conjunto completo de canciones.

```text
(pueden pegar un diagrama ASCII o una lista de clases)
Estructura del modelo:

  [ Cancion ]  -->  Atributos inmutables (id, titulo, artista, album, genero, anio, duracion_seg)
       |
       v
[ Catalogo (list) ]  -->  Estructura mutable que almacena la lista de canciones
```

## 3. Recursión (E2)

* **Función:** `versiones_de(relaciones, id_cancion)`
* **Caso base:** Si la canción no tiene versiones derivadas registradas en el diccionario `RELACIONES_VERSIONES`, la función retorna una lista vacía `[]`.
* **Caso recursivo:** Concatena las versiones directas con el resultado de llamar a `versiones_de()` para cada una de esas versiones.
* **Traza de un ejemplo real del dataset:**
  Para la Canción ID "1":
  * Llamada 1: `versiones_de("1")` -> tiene derivadas ["2", "3"]
    * Llamada 2: `versiones_de("2")` -> tiene derivada ["4"]
      * Llamada 3: `versiones_de("4")` -> caso base -> devuelve `[]`
      * Retorna `["4"]`
    * Llamada 4: `versiones_de("3")` -> caso base -> devuelve `[]`
    * Retorna `["3"]`
  * Resultado final: `["2", "3", "4"]`

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada | insertar al inicio, insertar al final, insertar ordenado, eliminar, buscar, iterar | El tamaño registrado coincide con la cantidad de nodos y la lista termina en None.|
| Pila |	apilar, desapilar, ver tope, esta vacía  | El último elemento agregado es el primero que se retira (LIFO). |
| Cola | encolar, desencolar, ver frente, esta vacía | El primer elemento agregado es el primero que se retira (FIFO). |

### Uso en el dominio
- ListaEnlazada: almacena las canciones de la playlist.
- Pila: conserva el historial de canciones consultadas.
- Cola: organiza las canciones pendientes de reproducción.

La pila y la cola utilizan internamente la lista enlazada.

## 5. Complejidad (E4)

| Operación | Tiempo | Espacio | Por qué |
| :--- | :---: | :---: | :--- |
| **Listar catálogo** | O(n) | O(1) | Recorre los n elementos de la lista enlazada mediante un iterador. |
| **Búsqueda lineal** | O(n) | O(1) | Toca cada elemento secuencialmente hasta encontrar el título o llegar al final. |
| **Búsqueda binaria** | O(log n) | O(1) | En cada iteración descarta la mitad del rango restante (requiere catálogo ordenado). |
| **Ordenar por selección** | O(n²) | O(1) | Bucle anidado que siempre realiza n(n-1)/2 comparaciones, sin importar el orden previo. |
| **Ordenar por inserción** | O(n²) peor / O(n) mejor | O(1) | En el peor caso desplaza todos los elementos; si ya está ordenado realiza 1 comparación por elemento. |
| **Buscar por ID** | O(n) | O(1) | Recorre los nodos de la lista enlazada secuencialmente hasta coincidir el ID. |

Mediciones (`time.perf_counter`):

| Operación | n | segundos |
| :--- | :---: | :---: |
| **búsqueda lineal (título)** | 5 | 0.000003 |
| **búsqueda lineal (n x 100)** | 500 | 0.000054 |
| **búsqueda binaria (título)** | 5 | 0.000002 |
| **búsqueda binaria (n x 100)** | 500 | 0.000004 |
| **ordenar por selección (título)** | 5 | 0.000008 |
| **ordenar por selección (n x 100)** | 500 | 0.018420 |
| **ordenar por inserción (año/duración)** | 5 | 0.000005 |
| **ordenar por inserción (n x 100)** | 500 | 0.015210 |

## 6. Persistencia (E5)

- Layout del registro binario: `struct.Struct("<I 30s 25s 30s 12s 2H")` = 105 bytes.
id (I, 4 B), titulo (30s, 30 B), artista (25s, 25 B), album (30s, 30 B), genero (12s, 12 B), anio (H, 2 B) y duracion_seg (H, 2 B). Cadenas UTF-8 recortadas/rellenadas con `\x00` al ancho fijo.
- Header: `struct.Struct("<4s 1s I")` = 9 bytes: magia `AYED`, tema `M`, cantidad de registros.
- Actualización por posición: `seek(HEADER.size + posicion * FORMATO.size)` y se pisa ese único registro (acceso directo, O(1)). El alta hace append al final y arregla la cantidad del header. La baja reescribe el archivo sin ese registro.

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
| Brenda | Entregas 1, 3 y 4 | Los contenidos y la implementación correspondientes a esas entregas. |
| Valentina | Entregas 2, 4 y 5 | Los contenidos y la implementación correspondientes a esas entregas. |
| Abril | Entrega 6. En el grupo anterior participó en las entregas 1, 2 y 3. | Las funcionalidades y documentación de la entrega 6, y su trabajo previo en las entregas 1, 2 y 3. |
8. Declaración de uso de inteligencia artificial

Se utilizó la IA como herramienta de apoyo durante el desarrollo del trabajo, principalmente para consultar dudas, revisar y corregir errores, mejorar la redacción de la documentación y comprender algunos aspectos de la implementación.