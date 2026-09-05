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


# copiamos las primeras filas del archivo data/canciones.csv
_CATALOGO_INICIAL = [
    Cancion("1", "De Musica Ligera", "Soda Stereo", "Cancion Animal", "Rock", 1990, 213),
    Cancion("2", "Persiana Americana", "Soda Stereo", "Signos", "Rock", 1986, 263),
    Cancion("3", "En la Ciudad de la Furia", "Soda Stereo", "Doble Vida", "Rock", 1988, 351),
    Cancion("4", "Crimen", "Gustavo Cerati", "Ahí vamos", "Rock", 2006, 239),
    Cancion("5", "Adios", "Gustavo Cerati", "Fuerza Natural", "Rock", 2009, 233)
]

def obtener_catalogo() -> list:
    """retorna la lista de canciones que forman el catalogo inicial."""
    return _CATALOGO_INICIAL