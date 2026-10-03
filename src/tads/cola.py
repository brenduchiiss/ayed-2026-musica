from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColaVaciaError

class Cola:
    """TAD cola implementado sobre ListaEnlazada."""

    def __init__(self):
        # usamos nuestra ListaEnlazada propia como contenedor interno
        self._lista = ListaEnlazada()

    def encolar(self, dato):
        """agrega un elemento al final de la cola."""
        self._lista.insertar_al_final(dato)

    def desencolar(self):
        """
        remueve y devuelve el primer elemento de la cola (la cabeza).
        lanza ColaVaciaError si la cola esta vacia.
        """
        if self.esta_vacia():
            raise ColaVaciaError("no se puede desencolar de una cola vacia.")

        frente = self._lista._cabeza.dato
        self._lista.eliminar(frente)
        return frente

    def ver_frente(self):
        """
        devuelve el primer elemento de la cola sin removerlo.
        lanza ColaVaciaError si la cola esta vacia.
        """
        if self.esta_vacia():
            raise ColaVaciaError("la cola esta vacia.")

        return self._lista._cabeza.dato

    def esta_vacia(self):
        """devuelve True si la cola no tiene elementos."""
        return self._lista.esta_vacia()
