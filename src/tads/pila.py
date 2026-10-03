from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import PilaVaciaError

class Pila:
    """TAD pila implementado sobre ListaEnlazada."""

    def __init__(self):
        # creamos una instancia de nuestra ListaEnlazada propia como atributo interno
        self._lista = ListaEnlazada()

    def apilar(self, dato):
        """agrega un elemento en el tope de la pila (al inicio de la lista)."""
        self._lista.insertar_al_inicio(dato)

    def desapilar(self):
        """
        remueve y devuelve el elemento del tope de la pila.
        lanza PilaVaciaError si la pila esta vacia.
        """
        if self.esta_vacia():
            raise PilaVaciaError("no se puede desapilar de una pila vacia.")

        tope = self._lista._cabeza.dato
        self._lista.eliminar(tope)
        return tope

    def ver_tope(self):
        """
        devuelve el elemento del tope sin removerlo.
        lanza PilaVaciaError si la pila esta vacia.
        """
        if self.esta_vacia():
            raise PilaVaciaError("la pila esta vacia.")

        return self._lista._cabeza.dato

    def esta_vacia(self):
        """devuelve True si la pila no tiene elementos."""
        return self._lista.esta_vacia()
