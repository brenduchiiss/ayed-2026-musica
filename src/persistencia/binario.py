"""Registros de longitud fija con struct.

Layout (documentar el definitivo en docs/INFORME.md):

Header (9 bytes):
  magia     4s   b'AYED'
  tema      1s   b'M' (musica)
  cantidad  I    unsigned int (4 bytes)

Registro de canción (105 bytes por registro):
  id           I    unsigned int (4 bytes)
  titulo      30s   bytes (30 bytes)
  artista     25s   bytes (25 bytes)
  album       30s   bytes (30 bytes)
  genero      12s   bytes (12 bytes)
  anio         H    unsigned short (2 bytes)
  duracion_seg H    unsigned short (2 bytes)
"""

import struct
from pathlib import Path
from src.excepciones import ArchivoInvalidoError, ItemNoEncontradoError
from src.tads.lista_enlazada import ListaEnlazada
from src.dominio.catalogo import Cancion, Catalogo

FORMATO = struct.Struct("<I 30s 25s 30s 12s 2H")
HEADER = struct.Struct("<4s 1s I")

TEMA = b"M" # musica

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
RUTA_BIN = DATA / "canciones.bin"

def _a_bytes(texto, ancho):
    # convierte texto a bytes UTF-8 y rellena con bytes nulos al ancho fijo
    return str(texto).encode("utf-8")[:ancho].ljust(ancho, b"\x00")

def _a_texto(datos):
    # convierte bytes a texto quitando el relleno de bytes nulos
    return datos.rstrip(b"\x00").decode("utf-8")

def _item_a_tupla(cancion):
    # convierte un objeto cancion a tupla para pack
    try:
        id_int = int(cancion.id)
    except ValueError:
        id_int = 0

    return (
        id_int,
        _a_bytes(cancion.titulo, 30),
        _a_bytes(cancion.artista, 25),
        _a_bytes(cancion.album, 30),
        _a_bytes(cancion.genero, 12),
        int(cancion.anio),
        int(cancion.duracion_seg),
    )


def _tupla_a_item(t):
    # convierte la tupla desempaquetada a un objeto cancion
    return Cancion(
        id_cancion=str(t[0]),
        titulo=_a_texto(t[1]),
        artista=_a_texto(t[2]),
        album=_a_texto(t[3]),
        genero=_a_texto(t[4]),
        anio=t[5],
        duracion_seg=t[6],
    )


def guardar_binario(ruta, items):
    """escribe la coleccion de canciones completa en el archivo binario"""
    ruta = Path(ruta)
    with open(ruta, "wb") as archivo:
        archivo.write(HEADER.pack(b"AYED", TEMA, len(items)))
        for cancion in items:
            archivo.write(FORMATO.pack(*_item_a_tupla(cancion)))


def cargar_binario(ruta):
    """lee el archivo binario validando header y registros truncados"""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo binario: {ruta}")

    with open(ruta, "rb") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado: header incompleto")

        magia, tema, cantidad = HEADER.unpack(cabecera)
        if magia != b"AYED":
            raise ArchivoInvalidoError("Magia incorrecta: este archivo no pertenece al programa.")
        if tema != TEMA:
            raise ArchivoInvalidoError(f"El tema del binario no coincide con Música ({TEMA!r}).")

        catalogo = Catalogo()
        for _ in range(cantidad):
            datos = archivo.read(FORMATO.size)
            if len(datos) < FORMATO.size:
                raise ArchivoInvalidoError("Binario truncado: faltan registros.")
            cancion = _tupla_a_item(FORMATO.unpack(datos))
            catalogo.agregar_cancion(cancion)

        return catalogo


def actualizar_registro(ruta, posicion, item):
    """pisa un registro por posicion (acceso directo). posicion es 0-based."""
    ruta = Path(ruta)
    with open(ruta, "r+b") as archivo:
        archivo.seek(HEADER.size + posicion * FORMATO.size)
        archivo.write(FORMATO.pack(*_item_a_tupla(item)))


def posicion_del_id(catalogo, id_buscado):
    """Devuelve la posición (0-based) del ítem con ese id, usando el iterador."""
    for posicion, item in enumerate(catalogo):
        if str(item.id) == str(id_buscado):
            return posicion
    raise ItemNoEncontradoError(f"No hay ítem con id {id_buscado}")


def alta_binario(ruta, item):
    """Agrega un registro AL FINAL y actualiza la cantidad del header."""
    ruta = Path(ruta)
    with open(ruta, "r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        magia, tema, cantidad = HEADER.unpack(cabecera)
        
        archivo.seek(0, 2) # 2 = saltar al FINAL del archivo
        archivo.write(FORMATO.pack(*_item_a_tupla(item)))
        
        archivo.seek(0) # volver al principio
        archivo.write(HEADER.pack(magia, tema, cantidad + 1)) # arreglar cantidad

def baja_binario(ruta, posicion):
    """Quita el registro 'posicion': relee, saca ese registro y reescribe todo."""
    ruta = Path(ruta)
    with open(ruta, "r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        magia, tema, cantidad = HEADER.unpack(cabecera)
        
        registros = [archivo.read(FORMATO.size) for _ in range(cantidad)]
        if 0 <= posicion < len(registros):
            del registros[posicion] # afuera el dado de baja
        
        archivo.seek(0)
        archivo.truncate() # borra el contenido viejo
        archivo.write(HEADER.pack(magia, tema, len(registros)))
        for datos in registros:
            archivo.write(datos)