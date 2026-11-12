from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColeccionLlenaError, ItemNoEncontradoError
from src.persistencia.texto import cargar_csv

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

    def eliminar_cancion(self, id_cancion: str):
        """Elimina una cancion por su ID reconstructiendo la lista enlazada."""
        encontrada = False
        nueva_lista = ListaEnlazada()
        for cancion in self._canciones:
            if str(cancion.id) == str(id_cancion) and not encontrada:
                encontrada = True
            else:
                nueva_lista.insertar_al_final(cancion)
        if not encontrada:
            raise ItemNoEncontradoError(f"No se encontró la canción con ID {id_cancion}")
        self._canciones = nueva_lista
    
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


# --- funciones de persistencia en texto (E5) ---
ENCABEZADOS = ["id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"]

def armar_catalogo_desde_txt(ruta):
    """Lee el .txt y devuelve un catalogo con objetos cancion."""
    filas = cargar_csv(ruta)
    cat = Catalogo(limite_maximo=100)
    for fila in filas:
        cancion = Cancion(
            id_cancion=str(fila["id"]),
            titulo=fila["titulo"],
            artista=fila["artista"],
            album=fila["album"],
            genero=fila["genero"],
            anio=int(fila["anio"]),
            duracion_seg=int(fila["duracion_seg"]),
        )
        cat.agregar_cancion(cancion)
    return cat


def filas_del_catalogo(catalogo):
    """Convierte las canciones del catalogo en dicts para guardar en .txt."""
    filas = []
    for c in catalogo:
        filas.append({
            "id": c.id,
            "titulo": c.titulo,
            "artista": c.artista,
            "album": c.album,
            "genero": c.genero,
            "anio": c.anio,
            "duracion_seg": c.duracion_seg,
        })
    return filas