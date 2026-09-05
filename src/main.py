from src.config import TEMA
from src.dominio.catalogo import obtener_catalogo

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")

def listar_catalogo():
    catalogo = obtener_catalogo()
    print("\n--- CATÁLOGO DE CANCIONES ---")
    if not catalogo:
        print("El catálogo está vacío.")
        return

    for cancion in catalogo:
        print(cancion)
    print("-" * 50)

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

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            # para la entrega 1: ejecutamos la func que muestra el catalogo cargado a mano
            listar_catalogo()
        elif opcion in {"2", "3", "4", "5", "6", "7", "8", "9"}:
            # las opciones de la 2 a la 9 quedan pendientes para las sig entregas del cuatri
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
