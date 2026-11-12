from src.config import TEMA
from src.excepciones import ArchivoInvalidoError, ItemNoEncontradoError, ColeccionLlenaError
from src.dominio.catalogo import (
    obtener_catalogo, versiones_de, RELACIONES_VERSIONES,
    Catalogo, Cancion, ENCABEZADOS, armar_catalogo_desde_txt, filas_del_catalogo
)
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion
from src.persistencia.texto import RUTA_TXT, guardar_csv
from src.persistencia.binario import (
    RUTA_BIN, guardar_binario, cargar_binario,
    actualizar_registro, posicion_del_id, alta_binario, baja_binario
)

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}

# Estado global del ordenamiento para la búsqueda binaria
_ORDENADO_POR = None  # Puede ser "titulo", "anio", "duracion_seg" o None


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")


def obtener_lista_canciones(catalogo):
    """Convierte el catálogo (ListaEnlazada) en una lista de Python para operar."""
    return [cancion for cancion in catalogo]


def reconstruir_catalogo(lista_canciones, limite_maximo=100):
    """Crea un nuevo objeto Catalogo cargando las canciones en el nuevo orden."""
    nuevo_cat = Catalogo(limite_maximo=limite_maximo)
    for c in lista_canciones:
        nuevo_cat.agregar_cancion(c)
    return nuevo_cat


def guardar_todo(catalogo):
    """Guarda el catálogo en los dos formatos. Memoria y archivos quedan iguales."""
    guardar_csv(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)
    guardar_binario(RUTA_BIN, catalogo)


def listar_catalogo(catalogo):
    print("\n--- CATÁLOGO DE CANCIONES ---")
    if not catalogo or len(catalogo) == 0:
        print("El catálogo está vacío.")
        return

    for cancion in catalogo:
        print(cancion)
    print("-" * 50)


def menu_buscar(catalogo):
    global _ORDENADO_POR
    print("\n--- MENÚ DE BÚSQUEDA ---")
    print("1) Buscar por Título (Búsqueda Lineal)")
    print("2) Buscar por Título (Búsqueda Binaria)")
    sub_opc = input("> ").strip()

    lista_canciones = obtener_lista_canciones(catalogo)
    if not lista_canciones:
        print("El catálogo está vacío.")
        return

    if sub_opc == "1":
        clave = input("Ingresá el título de la canción a buscar: ").strip()
        resultado = busqueda_lineal(
            lista_canciones,
            clave.lower(),
            obtener_clave=lambda c: c.titulo.lower()
        )
        if resultado:
            print(f"\n¡Canción encontrada!\n{resultado}")
        else:
            print(f"\nNo se encontró ninguna canción con el título '{clave}'.")

    elif sub_opc == "2":
        # REGLA DURA: Si no está ordenado por título, reordenamos y avisamos
        if _ORDENADO_POR != "titulo":
            print("\n[AVISO] El catálogo no estaba ordenado por título.")
            print("Ordenando automáticamente por Título (Selección) para poder aplicar búsqueda binaria...")
            ordenar_seleccion(lista_canciones, obtener_clave=lambda c: c.titulo.lower())
            _ORDENADO_POR = "titulo"
            # Actualizamos las canciones en el objeto catalogo
            catalogo = reconstruir_catalogo(lista_canciones, catalogo.limite_maximo)

        clave = input("Ingresá el título exacto de la canción a buscar (Binaria): ").strip()
        resultado = busqueda_binaria(
            lista_canciones,
            clave.lower(),
            obtener_clave=lambda c: c.titulo.lower()
        )
        if resultado:
            print(f"\n¡Canción encontrada!\n{resultado}")
        else:
            print(f"\nNo se encontró ninguna canción con el título '{clave}'.")
    else:
        print("Opción de búsqueda inválida.")


def menu_ordenar(catalogo):
    global _ORDENADO_POR
    print("\n--- MENÚ DE ORDENAMIENTO ---")
    print("1) Ordenar por Título (Selección - No Estable)")
    print("2) Ordenar por Año (Inserción - Estable)")
    print("3) Ordenar por Duración (Inserción - Estable)")
    sub_opc = input("> ").strip()

    lista_canciones = obtener_lista_canciones(catalogo)
    if not lista_canciones:
        print("El catálogo está vacío.")
        return catalogo

    if sub_opc == "1":
        ordenar_seleccion(lista_canciones, obtener_clave=lambda c: c.titulo.lower())
        _ORDENADO_POR = "titulo"
        print("\nCatálogo ordenado exitosamente por Título (Selección).")
    elif sub_opc == "2":
        ordenar_insercion(lista_canciones, obtener_clave=lambda c: c.anio)
        _ORDENADO_POR = "anio"
        print("\nCatálogo ordenado exitosamente por Año (Inserción).")
    elif sub_opc == "3":
        ordenar_insercion(lista_canciones, obtener_clave=lambda c: c.duracion_seg)
        _ORDENADO_POR = "duracion_seg"
        print("\nCatálogo ordenado exitosamente por Duración (Inserción).")
    else:
        print("Opción de ordenamiento inválida.")
        return catalogo

    nuevo_catalogo = reconstruir_catalogo(lista_canciones, catalogo.limite_maximo)
    guardar_todo(nuevo_catalogo)
    listar_catalogo(nuevo_catalogo)
    return nuevo_catalogo


def menu_archivos(catalogo):
    global _ORDENADO_POR
    print("\n--- GUARDAR / CARGAR Y ABM PERSISTENTE ---")
    print(" a) Cargar catálogo desde .txt")
    print(" b) Guardar catálogo en .txt")
    print(" c) Guardar catálogo en binario (.bin)")
    print(" d) Cargar catálogo desde binario (.bin)")
    print(" e) Alta de canción (persiste en .txt y .bin)")
    print(" f) Baja de canción por ID (persiste en .txt y .bin)")
    print(" g) Modificar canción por ID (acceso directo seek en .bin + .txt)")
    sub = input(" Subopción > ").strip().lower()

    try:
        if sub == "a":
            nombre = input("Archivo en data/ (Enter para canciones.txt): ").strip()
            ruta = (RUTA_TXT.parent / nombre) if nombre else RUTA_TXT
            catalogo = armar_catalogo_desde_txt(ruta)
            _ORDENADO_POR = None
            guardar_todo(catalogo)  # <--- ACÁ
            print(f"Catálogo cargado desde {ruta.name}: {len(catalogo)} ítems.")
        elif sub == "b":
            guardar_csv(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)
            print("Catálogo guardado en .txt.")
        elif sub == "c":
            guardar_binario(RUTA_BIN, catalogo)
            print("Catálogo guardado en .bin.")
        elif sub == "d":
            nombre = input("Archivo en data/ (Enter para canciones.bin): ").strip()
            ruta = (RUTA_BIN.parent / nombre) if nombre else RUTA_BIN
            catalogo = cargar_binario(ruta)
            _ORDENADO_POR = None
            guardar_todo(catalogo)  # <--- ACÁ
            print(f"Catálogo cargado desde {ruta.name}: {len(catalogo)} ítems.")
        elif sub == "e":
            id_c = input("ID: ").strip()
            titulo = input("Título: ").strip()
            artista = input("Artista: ").strip()
            album = input("Álbum: ").strip()
            genero = input("Género: ").strip()
            anio = int(input("Año: ").strip())
            dur = int(input("Duración (seg): ").strip())
            nueva = Cancion(id_c, titulo, artista, album, genero, anio, dur)
            catalogo.agregar_cancion(nueva)
            _ORDENADO_POR = None
            guardar_csv(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)
            if RUTA_BIN.exists():
                alta_binario(RUTA_BIN, nueva)
            else:
                guardar_binario(RUTA_BIN, catalogo)
            print("Canción agregada y guardada en archivos.")
        elif sub == "f":
            id_baja = input("ID de la canción a dar de baja: ").strip()
            pos = posicion_del_id(catalogo, id_baja)
            catalogo.eliminar_cancion(id_baja)
            _ORDENADO_POR = None
            guardar_csv(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)
            if RUTA_BIN.exists():
                baja_binario(RUTA_BIN, pos)
            print("Canción eliminada y cambios persistidos.")
        elif sub == "g":
            id_mod = input("ID de la canción a modificar: ").strip()
            pos = posicion_del_id(catalogo, id_mod)
            cancion_actual = catalogo.buscar_por_id(id_mod)
            print(f"Editando: {cancion_actual}")
            cancion_actual.titulo = input("Nuevo título (Enter para mantener): ").strip() or cancion_actual.titulo
            cancion_actual.artista = input("Nuevo artista (Enter para mantener): ").strip() or cancion_actual.artista
            cancion_actual.album = input("Nuevo álbum (Enter para mantener): ").strip() or cancion_actual.album
            cancion_actual.genero = input("Nuevo género (Enter para mantener): ").strip() or cancion_actual.genero
            anio_in = input("Nuevo año (Enter para mantener): ").strip()
            if anio_in:
                cancion_actual.anio = int(anio_in)
            dur_in = input("Nueva duración en seg (Enter para mantener): ").strip()
            if dur_in:
                cancion_actual.duracion_seg = int(dur_in)
            _ORDENADO_POR = None
            if not RUTA_BIN.exists():
                guardar_binario(RUTA_BIN, catalogo)
            actualizar_registro(RUTA_BIN, pos, cancion_actual)
            guardar_csv(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)
            print("Registro actualizado en .bin (acceso directo) y .txt.")
        else:
            print("Subopción inválida.")
    except (ArchivoInvalidoError, ItemNoEncontradoError, ColeccionLlenaError, ValueError) as error:
        print(f"Error: {error}")

    return catalogo


def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print()
    print(f"=== {nombre} — AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva")
    print("6. Colección principal (equipo / menú / playlist)")
    print("7. Historial (pila)")
    print("8. Cola")
    print("9. Guardar / cargar archivos")
    print("0. Salir")


def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return

    try:
        catalogo_actual = armar_catalogo_desde_txt(RUTA_TXT)
    except ArchivoInvalidoError:
        catalogo_actual = obtener_catalogo()

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            listar_catalogo(catalogo_actual)
        elif opcion == "3":
            menu_buscar(catalogo_actual)
        elif opcion == "4":
            catalogo_actual = menu_ordenar(catalogo_actual)
        elif opcion == "5":
            id_buscar = input("Ingrese el ID de la canción: ").strip()
            derivadas = versiones_de(RELACIONES_VERSIONES, id_buscar)
            if derivadas:
                print(f"Versiones derivadas de {id_buscar}: {derivadas}")
            else:
                print(f"La canción {id_buscar} no tiene versiones derivadas.")
        elif opcion in {"2", "6", "7", "8"}:
            pendiente()
        elif opcion == "9":
            catalogo_actual = menu_archivos(catalogo_actual)    
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
