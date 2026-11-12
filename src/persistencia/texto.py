from pathlib import Path
from src.excepciones import ArchivoInvalidoError

# modulo de lectura y escritura del .txt del catalogo
RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
RUTA_TXT = DATA / "canciones.txt"


def cargar_csv(ruta):
    """Carga secuencial. Devuelve una lista de dicts (E1 puede quedar así)."""
    # lee el txt linea por linea y devuelve la lista de diccionarios
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo: {ruta}")

    filas = []
    with ruta.open("r", encoding="utf-8") as archivo:
        linea_encabezado = archivo.readline()
        if not linea_encabezado:
            raise ArchivoInvalidoError(f"El archivo está vacío: {ruta}")
        
        encabezado = linea_encabezado.strip().split(",")
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            valores = linea.split(",")
            if len(valores) != len(encabezado):
                raise ArchivoInvalidoError(
                    f"Línea con {len(valores)} campos (se esperaban {len(encabezado)}): {linea}"
                )
            fila = dict(zip(encabezado, valores))
            filas.append(fila)

    return filas


def guardar_csv(ruta, filas, encabezados):
    """guarda la lista de diccionarios en un archivo de texto secuencial"""
    ruta = Path(ruta)
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        archivo.write(",".join(encabezados) + "\n")
        for fila in filas:
            campos = [str(fila[clave]) for clave in encabezados]
            archivo.write(",".join(campos) + "\n")