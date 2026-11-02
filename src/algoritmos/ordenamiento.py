"""
Módulo de algoritmos de ordenamiento propio para AyED C2 2026.
Prohibido usar 'sorted()' o '.sort()' para cumplir la consigna.
"""

def ordenar_seleccion(coleccion, obtener_clave=None):
    """
    Ordena la colección in-place mediante Selección (NO estable).
    Complejidad: O(n²) en todos los casos.
    """
    n = len(coleccion)
    for i in range(n - 1):
        pos_min = i
        for j in range(i + 1, n):
            val_j = coleccion[j] if obtener_clave is None else obtener_clave(coleccion[j])
            val_min = coleccion[pos_min] if obtener_clave is None else obtener_clave(coleccion[pos_min])
            if val_j < val_min:
                pos_min = j
        coleccion[i], coleccion[pos_min] = coleccion[pos_min], coleccion[i]
    return coleccion


def ordenar_insercion(coleccion, obtener_clave=None):
    """
    Ordena la colección in-place mediante Inserción (ESTABLE).
    Complejidad: O(n) mejor caso, O(n²) peor/promedio.
    """
    n = len(coleccion)
    for i in range(1, n):
        actual = coleccion[i]
        val_actual = actual if obtener_clave is None else obtener_clave(actual)
        j = i - 1

        while j >= 0:
            val_j = coleccion[j] if obtener_clave is None else obtener_clave(coleccion[j])
            if val_j > val_actual:
                coleccion[j + 1] = coleccion[j]
                j -= 1
            else:
                break
        coleccion[j + 1] = actual
    return coleccion
