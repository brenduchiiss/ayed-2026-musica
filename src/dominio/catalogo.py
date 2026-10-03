from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColeccionLlenaError, ItemNoEncontradoError

class Cancion:
    """clase que representa una cancion individual dentro del catalogo."""
    def __init__(self, id_cancion: str, titulo: str, artista: str, album: str, genero: str, anio: int, duracion_seg: int):
        self.id = id_cancion
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.genero = genero
        self.anio = int(anio)
        self.duracion_seg = int(duracion_seg)

    def __str__(self) -> str:
        # convertimos duracion_seg a minutos y segundos para mostrarlo mas prolijo en la pantalla
        minutos = self.duracion_seg // 60
        segundos = self.duracion_seg % 60
        return f"[{self.id}] '{self.titulo}' - {self.artista} | Álbum: {self.album} | Género: {self.genero} | Año: {self.anio} | Duración: {minutos}:{segundos:02d} min"

class Catalogo:
    """coleccion principal del dominio sobre ListaEnlazada con limite maximo (tope)."""

    def __init__(self, limite_maximo: int = 100):
        self._canciones = ListaEnlazada()
        self.limite_maximo = limite_maximo

    def agregar_cancion(self, cancion: Cancion):
        """
        agrega una cancion al catalogo.
        Lanza ColeccionLlenaError si se intenta superar el limite.
        """
        if self._canciones.tamanio() >= self.limite_maximo:
            raise ColeccionLlenaError(f"El catalogo esta lleno. Limite maximo: {self.limite_maximo}")
        self._canciones.insertar_al_final(cancion)

    def buscar_por_id(self, id_cancion: str) -> Cancion:
        """
        busca una cancion por su ID recorriendo la lista enlazada.
        lanza ItemNoEncontradoError si no existe.
        """
        for cancion in self._canciones:
            if cancion.id == id_cancion:
                return cancion
        raise ItemNoEncontradoError(f"No se encontro la cancion con ID {id_cancion}")

    def __iter__(self):
        """permite iterar sobre las canciones del catalogo usando el iterador de ListaEnlazada."""
        return iter(self._canciones)

    def __len__(self):
        """devuelve la cantidad de canciones en el catalogo."""
        return self._canciones.tamanio()

# copiamos las primeras filas del archivo data/canciones.csv
_CATALOGO_INICIAL = [
    Cancion("1", "De Musica Ligera", "Soda Stereo", "Cancion Animal", "Rock", 1990, 213),
    Cancion("2", "Persiana Americana", "Soda Stereo", "Signos", "Rock", 1986, 263),
    Cancion("3", "En la Ciudad de la Furia", "Soda Stereo", "Doble Vida", "Rock", 1988, 351),
    Cancion("4", "Crimen", "Gustavo Cerati", "Ahí vamos", "Rock", 2006, 239),
    Cancion("5", "Adios", "Gustavo Cerati", "Fuerza Natural", "Rock", 2009, 233)
]

def obtener_catalogo():
    """retorna un catalogo construido sobre ListaEnlazada con las canciones iniciales."""
    catalogo = Catalogo(limite_maximo=100)
    for cancion in _CATALOGO_INICIAL:
        catalogo.agregar_cancion(cancion)
    return catalogo

# Diccionario de versiones para la recursión (ID original -> lista de versiones)
RELACIONES_VERSIONES = {
    "1": ["2", "3"],
    "2": ["4"],
    "3": [],
    "4": []
}

def versiones_de(relaciones, id_cancion):
    directas = relaciones.get(id_cancion, [])
    # CASO BASE: si no tiene derivadas, devuelve lista vacía
    if not directas:
        return []
    # CASO RECURSIVO: busca las versiones de las versiones
    resultado = list(directas)
    for v in directas:
        resultado += versiones_de(relaciones, v)
    return resultado
