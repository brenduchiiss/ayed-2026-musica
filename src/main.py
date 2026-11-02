from src.config import TEMA
from src.dominio.catalogo import obtener_catalogo, versiones_de, RELACIONES_VERSIONES, Catalogo, Cancion
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion

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
    listar_catalogo(nuevo_catalogo)
    return nuevo_catalogo


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
        elif opcion in {"2", "6", "7", "8", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
