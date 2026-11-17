
# TP integrador — AyED C2 2026

Repositorio del grupo. Partir de este esqueleto. No borrar la estructura de `src/` ni de `docs/`.

- **Consigna en el navegador:** https://algoritmos-unab.github.io/ayed-c2-2026-tp/
- **Repositorio:** https://github.com/algoritmos-UNaB/ayed-c2-2026-tp
- **Esqueleto:** `tp-integrador/esqueleto`
- Regenerar el sitio: `py -3 tools/build_site.py` (hace falta el paquete `markdown`).

## Integrantes

| Nombre | Mail | GitHub |
| :--- | :--- | :--- |
| Brenda Correa | brendamcorrea.25@gmail.com | brenduchiiss |
| Abril Gomez | abrilagostinagomez34@gmail.com | abrilagostinagomez3456 |
| Valentina Skrobacki | valentinaskrobacki@gmail.com | valentinaskrobacki |

**Tema elegido:** Biblioteca musical.

## Cómo ejecutar

Desde la raíz del repositorio, con Python 3.10 o superior:

```text
python -m src.main
```

En Windows, si `python` no anda: `py -3 -m src.main`.

El proyecto utiliza únicamente la biblioteca estándar de Python. No requiere `requirements.txt`.

## Funcionalidades

- Listar el catálogo musical.
- Consultar detalles de canciones.
- Buscar canciones mediante búsqueda lineal y binaria.
- Ordenar canciones por distintos criterios.
- Consultar versiones relacionadas mediante recursividad.
- Administrar colecciones de canciones.
- Gestionar el historial mediante una pila.
- Gestionar canciones pendientes mediante una cola.
- Guardar y cargar información en archivos TXT y binarios.

## Persistencia

El programa permite guardar y cargar el catálogo en archivos de texto y binarios. Los archivos binarios utilizan registros de longitud fija y permiten actualizar registros por posición.

## Limitaciones

El programa funciona mediante una interfaz de consola. No cuenta con interfaz gráfica. Los archivos binarios de prueba se generan desde el propio programa.

## Entregas

Cada vencimiento se marca con un tag. Ver `GIT.md`.

| Tag | Vence |
| --- | --- |
| `preentrega` (opcional, solo repo) | domingo 30-ago-2026 23:59 |
| `entrega-1` | domingo 06-sep-2026 23:59 |
| `entrega-2` | domingo 20-sep-2026 23:59 |
| `entrega-3` | domingo 04-oct-2026 23:59 |
| `entrega-4` | domingo 01-nov-2026 23:59 |
| `entrega-5` | domingo 15-nov-2026 23:59 |
| `entrega-6` | domingo 22-nov-2026 23:59 |

Defensa oral (reemplaza el 2do parcial): 25 y 27-nov-2026.

La cátedra corrige el **tag**, no el último commit suelto de `main`.

El grupo se avisa por mail a diego.ambrossio@unab.edu.ar **y** angel.bianco@unab.edu.ar. Ver `GIT.md`.