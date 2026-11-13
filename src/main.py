
from src.config import TEMA
from src.excepciones import (
    ArchivoInvalidoError,
    ItemNoEncontradoError,
    ColeccionLlenaError
)
from src.dominio.catalogo import (
    obtener_catalogo,
    versiones_de,
    RELACIONES_VERSIONES,
    Catalogo,
    Cancion,
    ENCABEZADOS,
    armar_catalogo_desde_txt,
    filas_del_catalogo
)
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion
from src.persistencia.texto import RUTA_TXT, guardar_csv
from src.persistencia.binario import (
    RUTA_BIN,
    guardar_binario,
    cargar_binario,
    actualizar_registro,
    posicion_del_id,
    alta_binario,
    baja_binario
)
from src.dominio.playlist import Playlist
from src.tads.pila import Pila
from src.tads.cola import Cola


TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}

_ORDENADO_POR = None


def menu_playlist(catalogo, playlist):
    while True:
        print("\n--- MENÚ PLAYLIST ---")
        print("1. Agregar canción")
        print("2. Mostrar playlist")
        print("3. Eliminar canción")
        print("0. Volver al menú principal")

        opcion = input("> ").strip()

        if opcion == "1":
            id_cancion = input("Ingresá el ID de la canción: ").strip()

            try:
                cancion = catalogo.buscar_por_id(id_cancion)

                if playlist.agregar_cancion(cancion):
                    print("Canción agregada a la playlist.")
                else:
                    print("Esa canción ya está en la playlist.")

            except ItemNoEncontradoError as error:
                print(f"Error: {error}")

        elif opcion == "2":
            if playlist.esta_vacia():
                print("La playlist está vacía.")
            else:
                print("\n--- CANCIONES DE LA PLAYLIST ---")
                for cancion in playlist:
                    print(cancion)

        elif opcion == "3":
            id_cancion = input(
                "Ingresá el ID de la canción que querés eliminar: "
            ).strip()

            if playlist.eliminar_cancion(id_cancion):
                print("Canción eliminada.")
            else:
                print("No se encontró esa canción en la playlist.")

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")


def menu_historial(historial):
    while True:
        print("\n--- MENÚ HISTORIAL ---")
        print("1. Ver última consulta")
        print("2. Deshacer última consulta")
        print("3. Mostrar si el historial está vacío")
        print("0. Volver al menú principal")

        opcion = input("> ").strip()

        if opcion == "1":
            if historial.esta_vacia():
                print("El historial está vacío.")
            else:
                print("\nÚltima canción consultada:")
                print(historial.ver_tope())

        elif opcion == "2":
            if historial.esta_vacia():
                print("No hay consultas para deshacer.")
            else:
                cancion = historial.desapilar()
                print(f"Se quitó del historial: {cancion}")

        elif opcion == "3":
            if historial.esta_vacia():
                print("El historial está vacío.")
            else:
                print("El historial contiene consultas.")

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")


def menu_cola(catalogo, cola):
    while True:
        print("\n--- MENÚ COLA ---")
        print("1. Agregar canción a la cola")
        print("2. Ver próxima canción")
        print("3. Atender próxima canción")
        print("4. Mostrar si la cola está vacía")
        print("0. Volver al menú principal")

        opcion = input("> ").strip()

        if opcion == "1":
            id_cancion = input("Ingresá el ID de la canción: ").strip()

            try:
                cancion = catalogo.buscar_por_id(id_cancion)
                cola.encolar(cancion)
                print(f"Canción agregada a la cola: {cancion}")

            except ItemNoEncontradoError as error:
                print(f"Error: {error}")

        elif opcion == "2":
            if cola.esta_vacia():
                print("La cola está vacía.")
            else:
                print("\nPróxima canción:")
                print(cola.ver_frente())

        elif opcion == "3":
            if cola.esta_vacia():
                print("No hay canciones para atender.")
            else:
                cancion = cola.desencolar()
                print(f"Canción atendida: {cancion}")

        elif opcion == "4":
            if cola.esta_vacia():
                print("La cola está vacía.")
            else:
                print("La cola contiene canciones pendientes.")

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")


def menu_detalle(catalogo):
    id_cancion = input("Ingresá el ID de la canción: ").strip()

    try:
        cancion = catalogo.buscar_por_id(id_cancion)
        print("\n--- DETALLE DE LA CANCIÓN ---")
        print(cancion)

    except ItemNoEncontradoError as error:
        print(f"Error: {error}")


def obtener_lista_canciones(catalogo):
    """Convierte el catálogo en una lista de Python para operar."""
    return [cancion for cancion in catalogo]


def reconstruir_catalogo(lista_canciones, limite_maximo=100):
    """Crea un nuevo catálogo con las canciones en el nuevo orden."""
    nuevo_cat = Catalogo(limite_maximo=limite_maximo)

    for cancion in lista_canciones:
        nuevo_cat.agregar_cancion(cancion)

    return nuevo_cat


def guardar_todo(catalogo):
    """Guarda el catálogo en los dos formatos."""
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
        return catalogo

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
        if _ORDENADO_POR != "titulo":
            print("\n[AVISO] El catálogo no estaba ordenado por título.")
            print(
                "Ordenando automáticamente por Título "
                "(Selección) para aplicar búsqueda binaria..."
            )

            ordenar_seleccion(
                lista_canciones,
                obtener_clave=lambda c: c.titulo.lower()
            )

            _ORDENADO_POR = "titulo"
            catalogo = reconstruir_catalogo(
                lista_canciones,
                catalogo.limite_maximo
            )

        clave = input(
            "Ingresá el título exacto de la canción a buscar (Binaria): "
        ).strip()

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

    return catalogo


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
        ordenar_seleccion(
            lista_canciones,
            obtener_clave=lambda c: c.titulo.lower()
        )
        _ORDENADO_POR = "titulo"
        print("\nCatálogo ordenado exitosamente por Título (Selección).")

    elif sub_opc == "2":
        ordenar_insercion(
            lista_canciones,
            obtener_clave=lambda c: c.anio
        )
        _ORDENADO_POR = "anio"
        print("\nCatálogo ordenado exitosamente por Año (Inserción).")

    elif sub_opc == "3":
        ordenar_insercion(
            lista_canciones,
            obtener_clave=lambda c: c.duracion_seg
        )
        _ORDENADO_POR = "duracion_seg"
        print("\nCatálogo ordenado exitosamente por Duración (Inserción).")

    else:
        print("Opción de ordenamiento inválida.")
        return catalogo

    nuevo_catalogo = reconstruir_catalogo(
        lista_canciones,
        catalogo.limite_maximo
    )

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
            nombre = input(
                "Archivo en data/ (Enter para canciones.txt): "
            ).strip()

            ruta = (RUTA_TXT.parent / nombre) if nombre else RUTA_TXT
            catalogo = armar_catalogo_desde_txt(ruta)
            _ORDENADO_POR = None
            guardar_todo(catalogo)

            print(
                f"Catálogo cargado desde {ruta.name}: "
                f"{len(catalogo)} ítems."
            )

        elif sub == "b":
            guardar_csv(
                RUTA_TXT,
                filas_del_catalogo(catalogo),
                ENCABEZADOS
            )
            print("Catálogo guardado en .txt.")

        elif sub == "c":
            guardar_binario(RUTA_BIN, catalogo)
            print("Catálogo guardado en .bin.")

        elif sub == "d":
            nombre = input(
                "Archivo en data/ (Enter para canciones.bin): "
            ).strip()

            ruta = (RUTA_BIN.parent / nombre) if nombre else RUTA_BIN
            catalogo = cargar_binario(ruta)
            _ORDENADO_POR = None
            guardar_todo(catalogo)

            print(
                f"Catálogo cargado desde {ruta.name}: "
                f"{len(catalogo)} ítems."
            )

        elif sub == "e":
            id_c = input("ID: ").strip()
            titulo = input("Título: ").strip()
            artista = input("Artista: ").strip()
            album = input("Álbum: ").strip()
            genero = input("Género: ").strip()
            anio = int(input("Año: ").strip())
            dur = int(input("Duración (seg): ").strip())

            nueva = Cancion(
                id_c, titulo, artista, album, genero, anio, dur
            )

            catalogo.agregar_cancion(nueva)
            _ORDENADO_POR = None

            guardar_csv(
                RUTA_TXT,
                filas_del_catalogo(catalogo),
                ENCABEZADOS
            )

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

            guardar_csv(
                RUTA_TXT,
                filas_del_catalogo(catalogo),
                ENCABEZADOS
            )

            if RUTA_BIN.exists():
                baja_binario(RUTA_BIN, pos)

            print("Canción eliminada y cambios persistidos.")

        elif sub == "g":
            id_mod = input("ID de la canción a modificar: ").strip()
            pos = posicion_del_id(catalogo, id_mod)
            cancion_actual = catalogo.buscar_por_id(id_mod)

            print(f"Editando: {cancion_actual}")

            cancion_actual.titulo = (
                input("Nuevo título (Enter para mantener): ").strip()
                or cancion_actual.titulo
            )

            cancion_actual.artista = (
                input("Nuevo artista (Enter para mantener): ").strip()
                or cancion_actual.artista
            )

            cancion_actual.album = (
                input("Nuevo álbum (Enter para mantener): ").strip()
                or cancion_actual.album
            )

            cancion_actual.genero = (
                input("Nuevo género (Enter para mantener): ").strip()
                or cancion_actual.genero
            )

            anio_in = input(
                "Nuevo año (Enter para mantener): "
            ).strip()

            if anio_in:
                cancion_actual.anio = int(anio_in)

            dur_in = input(
                "Nueva duración en seg (Enter para mantener): "
            ).strip()

            if dur_in:
                cancion_actual.duracion_seg = int(dur_in)

            _ORDENADO_POR = None

            if not RUTA_BIN.exists():
                guardar_binario(RUTA_BIN, catalogo)

            actualizar_registro(RUTA_BIN, pos, cancion_actual)

            guardar_csv(
                RUTA_TXT,
                filas_del_catalogo(catalogo),
                ENCABEZADOS
            )

            print(
                "Registro actualizado en .bin "
                "(acceso directo) y .txt."
            )

        else:
            print("Subopción inválida.")

    except (
        ArchivoInvalidoError,
        ItemNoEncontradoError,
        ColeccionLlenaError,
        ValueError
    ) as error:
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
        print(
            "Seteá TEMA en src/config.py: "
            "'pokedex', 'recetario' o 'musica'."
        )
        return

    try:
        catalogo_actual = armar_catalogo_desde_txt(RUTA_TXT)
    except ArchivoInvalidoError:
        catalogo_actual = obtener_catalogo()

    playlist = Playlist()
    historial = Pila()
    cola = Cola()

    opcion = None

    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()

        if opcion == "0":
            print("Chau.")

        elif opcion == "1":
            listar_catalogo(catalogo_actual)

        elif opcion == "2":
            menu_detalle(catalogo_actual)

        elif opcion == "3":
            catalogo_actual = menu_buscar(catalogo_actual)

        elif opcion == "4":
            catalogo_actual = menu_ordenar(catalogo_actual)

        elif opcion == "5":
            id_buscar = input(
                "Ingrese el ID de la canción: "
            ).strip()

            try:
                cancion = catalogo_actual.buscar_por_id(id_buscar)
                historial.apilar(cancion)

                print(f"Consulta registrada: {cancion}")

                derivadas = versiones_de(
                    RELACIONES_VERSIONES,
                    id_buscar
                )

                if derivadas:
                    print(
                        f"Versiones derivadas de {id_buscar}: "
                        f"{derivadas}"
                    )
                else:
                    print(
                        f"La canción {id_buscar} "
                        "no tiene versiones derivadas."
                    )

            except ItemNoEncontradoError as error:
                print(f"Error: {error}")

        elif opcion == "6":
            menu_playlist(catalogo_actual, playlist)

        elif opcion == "7":
            menu_historial(historial)

        elif opcion == "8":
            menu_cola(catalogo_actual, cola)

        elif opcion == "9":
            catalogo_actual = menu_archivos(catalogo_actual)

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
