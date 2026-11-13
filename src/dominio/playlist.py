from src.tads.lista_enlazada import ListaEnlazada


class Playlist:
    """Playlist de canciones implementada mediante una lista enlazada."""

    def __init__(self):
        self._canciones = ListaEnlazada()

    def agregar_cancion(self, cancion):
        """Agrega una canción si todavía no está en la playlist."""
        for actual in self._canciones:
            if actual.id == cancion.id:
                return False

        self._canciones.insertar_al_final(cancion)
        return True

    def eliminar_cancion(self, id_cancion):
        """Elimina una canción de la playlist utilizando su ID."""
        for cancion in self._canciones:
            if str(cancion.id) == str(id_cancion):
                return self._canciones.eliminar(cancion)

        return False

    def esta_vacia(self):
        return self._canciones.esta_vacia()

    def tamanio(self):
        return self._canciones.tamanio()

    def __iter__(self):
        return iter(self._canciones)
