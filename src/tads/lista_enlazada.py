class Nodo:
    """Nodo individual para una lista enlazada simple."""
    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class ListaEnlazada:
    """TAD lista enlazada simple. No usar list de Python por debajo."""


    def __init__(self):
        self._cabeza = None
        self._tamanio = 0


    def esta_vacia(self):
        """devuelve True si la lista no tiene elementos, False en caso contrario."""
        return self._cabeza is None


    def tamanio(self):
        """devuelve la cantidad de elementos en la lista."""
        return self._tamanio


    def insertar_al_inicio(self, dato):
        """crea un nuevo nodo y lo coloca al principio de la lista."""
        nuevo_nodo = Nodo(dato, siguiente=self._cabeza)
        self._cabeza = nuevo_nodo
        self._tamanio += 1


    def insertar_al_final(self, dato):
        """crea un nuevo nodo y lo coloca al final de la lista."""
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self._cabeza = nuevo_nodo
        else:
            actual = self._cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self._tamanio += 1


    def insertar_ordenado(self, dato, clave):
        """
        nnserta un dato manteniendo el orden ascendente segun el valor devuelto por la funcion 'clave'.
        por ejemplo, clave puede ser lambda x: x.titulo.
        """
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia() or clave(dato) < clave(self._cabeza.dato):
            nuevo_nodo.siguiente = self._cabeza
            self._cabeza = nuevo_nodo
        else:
            actual = self._cabeza
            while actual.siguiente is not None and clave(actual.siguiente.dato) <= clave(dato):
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo
        self._tamanio += 1


    def eliminar(self, dato):
        """
        elimina la primera aparicion de 'dato' en la lista.
        devuelve True si lo encontro y elimino, o False si no estaba.
        """
        if self.esta_vacia():
            return False


        if self._cabeza.dato == dato:
            self._cabeza = self._cabeza.siguiente
            self._tamanio -= 1
            return True


        actual = self._cabeza
        while actual.siguiente is not None:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self._tamanio -= 1
                return True
            actual = actual.siguiente


        return False


    def buscar(self, dato):
        """devuelve el dato si lo encuentra en la lista, o None si no existe."""
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                return actual.dato
            actual = actual.siguiente
        return None


    def __iter__(self):
        """permite iterar la lista directamente en un bucle for usando yield."""
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente


