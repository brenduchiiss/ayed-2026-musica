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

- Función:
- Caso base:
- Caso recursivo:
- Traza de un ejemplo real del dataset:

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada |  |  |
| Pila |  |  |
| Cola |  |  |

Dónde se usa cada uno en el dominio.

## 5. Complejidad (E4)

| Operación | Tiempo | Espacio | Por qué |
| --- | --- | --- | --- |
|  |  |  |  |

Mediciones (`time.perf_counter`):

| Operación | n | segundos |
| --- | --- | --- |
|  |  |  |

## 6. Persistencia (E5)

- Layout del registro binario (campos, `struct`, anchos):
- Header:
- Cómo se actualiza un registro por posición:

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
|  |  |  |
