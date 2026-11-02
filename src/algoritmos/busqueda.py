"""
Módulo de algoritmos de búsqueda propia para AyED C2 2026.
Prohibido usar 'in', '.index()' o 'bisect' para cumplir la consigna.
"""

def busqueda_lineal(coleccion, clave, obtener_clave=None):
    """
    Realiza una búsqueda lineal elemento por elemento.
    Funciona sobre colecciones desordenadas u ordenadas.
    Retorna el elemento encontrado o None si no existe.
    """
    for elemento in coleccion:
        valor = elemento if obtener_clave is None else obtener_clave(elemento)
        if valor == clave:
            return elemento
    return None


def busqueda_binaria(coleccion, clave, obtener_clave=None):
    """
    Realiza una búsqueda binaria dividiendo el rango a la mitad.
    REQUIERE que la colección esté previamente ordenada por la clave buscada.
    Retorna el elemento encontrado o None si no existe.
    """
    izq = 0
    der = len(coleccion) - 1

    while izq <= der:
        medio = (izq + der) // 2
        elemento = coleccion[medio]
        valor = elemento if obtener_clave is None else obtener_clave(elemento)

        if valor == clave:
            return elemento
        elif valor < clave:
            izq = medio + 1
        else:
            der = medio - 1

    return None
