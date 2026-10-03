from src.config import TEMA
from src.dominio.catalogo import obtener_catalogo, versiones_de, RELACIONES_VERSIONES, Cancion
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.excepciones import (
    ColeccionLlenaError,
    ItemNoEncontradoError,
    PilaVaciaError,
    ColaVaciaError
)

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")

def listar_catalogo(catalogo):
    print("\n--- CATÁLOGO DE CANCIONES ---")
    if len(catalogo) == 0:
        print("El catálogo está vacío.")
        return

    # utiliza el iterador implementado en Catalogo y ListaEnlazada
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

    # instanciamos los TADs para el dominio de la aplicacion
    catalogo = obtener_catalogo()
    historial_pila = Pila()
    reproduccion_cola = Cola()

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            listar_catalogo(catalogo)
        elif opcion == "5":
            id_buscar = input("Ingrese el ID de la canción: ").strip()
            derivadas = versiones_de(RELACIONES_VERSIONES, id_buscar)
            if derivadas:
                print(f"Versiones derivadas de {id_buscar}: {derivadas}")
            else:
                print(f"La canción {id_buscar} no tiene versiones derivadas.")
        elif opcion == "6":
            print("\n--- AGREGAR CANCIÓN A LA COLECCIÓN ---")
            id_c = input("ID: ").strip()
            titulo = input("Título: ").strip()
            artista = input("Artista: ").strip()
            album = input("Álbum: ").strip()
            genero = input("Género: ").strip()
            try:
                anio = int(input("Año: ").strip())
                duracion = int(input("Duración en segundos: ").strip())
                nueva_cancion = Cancion(id_c, titulo, artista, album, genero, anio, duracion)
                catalogo.agregar_cancion(nueva_cancion)
                print(f"¡Canción '{titulo}' agregada con éxito al catálogo!")
            except ValueError:
                print("Error: El año y la duracion deben ser numeros enteros.")
            except ColeccionLlenaError as e:
                print(f"Error de Capacidad: {e}")
        elif opcion == "7":
            print("\n--- HISTORIAL DE REPRODUCCIÓN (PILA) ---")
            print("a) Reproducir cancion (apilar)")
            print("b) Deshacer ultima reproduccion (desapilar)")
            print("c) Ver ultima cancion reproducida (ver tope)")
            sub_op = input("> ").strip().lower()
            try:
                if sub_op == "a":
                    id_c = input("Ingrese el ID de la cancion a reproducir: ").strip()
                    cancion = catalogo.buscar_por_id(id_c)
                    historial_pila.apilar(cancion)
                    print(f"Reproduciendo: {cancion}")
                elif sub_op == "b":
                    cancion_sacada = historial_pila.desapilar()
                    print(f"Deshecha la reproduccion de: {cancion_sacada}")
                elif sub_op == "c":
                    tope = historial_pila.ver_tope()
                    print(f"Ultima cancion en el historial: {tope}")
                else:
                    print("Subopcion invalida.")
            except ItemNoEncontradoError as e:
                print(f"Error de Busqueda: {e}")
            except PilaVaciaError as e:
                print(f"Error de Historial: {e}")
        elif opcion == "8":
            print("\n--- COLA DE REPRODUCCIÓN (COLA) ---")
            print("a) Encolar cancion")
            print("b) Reproducir siguiente (desencolar)")
            print("c) Ver siguiente en la cola (ver frente)")
            sub_op = input("> ").strip().lower()
            try:
                if sub_op == "a":
                    id_c = input("Ingrese el ID de la cancion a encolar: ").strip()
                    cancion = catalogo.buscar_por_id(id_c)
                    reproduccion_cola.encolar(cancion)
                    print(f"Cancion '{cancion.titulo}' agregada a la cola.")
                elif sub_op == "b":
                    siguiente = reproduccion_cola.desencolar()
                    print(f"Reproduciendo de la cola: {siguiente}")
                    # Al reproducir, la agregamos automáticamente al historial (Pila)
                    historial_pila.apilar(siguiente)
                elif sub_op == "c":
                    frente = reproduccion_cola.ver_frente()
                    print(f"Siguiente cancion en la cola: {frente}")
                else:
                    print("Subopcion invalida.")
            except ItemNoEncontradoError as e:
                print(f"Error de Busqueda: {e}")
            except ColaVaciaError as e:
                print(f"Error de Cola: {e}")

        elif opcion in {"2", "3", "4", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
