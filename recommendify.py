import sys
import csv
import operaciones as op
from errores import *
from grafos import Grafo


def crear_grafo_desde_tsv(ruta):
    """
    Si existe, abre un tsv para cargar su información a dos grafos de la siguiente forma:
    Nuestros campos son: ID    USER_ID	TRACK_NAME	ARTIST	PLAYLIST_ID PLAYLIST_NAME	GENRES
    Grafo bipartito de Canciones y Usuarios relacionada a partir de playlists:
        -Crea un vértice (v) con el USER_ID
        -Crea otro vértice (w) como TRACK_NAME - ARTIST
        -Une ambos vertices con una arista que de peso (p) tiene PLAYLIST_NAME
    Grafo que relaciona Canciones a partir de Playlists
        -Crea un vertice (w) como TRACK_NAME - ARTIST
        -Crea aristas entre este vertice y todos los demas que compartan playlist, sin peso
    """
    canciones_usuarios, canciones_playlist = Grafo()
    with open(ruta) as archivo_tsv:
        # Mira si la primer linea es un encabezado, de ser así la ignora.
        tiene_encabezado = csv.Sniffer().has_header(archivo_tsv.read(1024))
        archivo_tsv.seek(0)  # Volver al comienzo del archivo.
        lector = csv.reader(archivo_tsv, delimiter="\t")
        if tiene_encabezado:
            next(lector)
        playlist_actual = None
        comparten_playlist = []
        for fila in lector:
            # Grafo bipartito
            v = fila[1]
            w = fila[2] + ' - ' + fila[3]
            p = fila[5]
            canciones_usuarios.agregar_vertice(v)
            canciones_usuarios.agregar_vertice(w)
            canciones_usuarios.agregar_arista(v, w, p)
            # El otro grafo
            if playlist_actual == fila[4]:
                comparten_playlist.append(w)
            else:
                playlist_actual = fila[4]
                comparten_playlist = []
            canciones_playlist.agregar_vertice(w)
            for i in comparten_playlist:
                canciones_playlist.agregar_arista(comparten_playlist[i], w)
    return canciones_usuarios, canciones_playlist


def procesar_comandos(comando, parametros, canciones_usuarios, canciones_playlist):
    """
    Comprueba si los comandos existen.
    Si lo estan, ejecuta el comando enviado, dandole los parametros y el grafo que les corresponda.
    Si no, devuelve error.
    """
    if comando not in op.COMANDOS:
        print(ERR_CMD)
        return
    tipo_grafo = op.COMANDOS.get(comando)
    if tipo_grafo == op.GRAFO_USUARIOS:
        getattr(op, comando)(canciones_usuarios, parametros)
    else:
        getattr(op, comando)(canciones_playlist, parametros)


def procesar_entrada(canciones_usuarios, canciones_playlist):
    """Separa la entrada en el comando y sus respectivos parametros, luego los procesa"""
    for linea in sys.stdin:
        parse = linea.split()
        if len(parse) > 0:
            comando = parse[0]
            parametros = []
            if len(parse) > 1:
                parametros = ' '.join(parse[1:])
            procesar_comandos(comando, parametros, canciones_usuarios, canciones_playlist)
        else:
            print(ERR_CMD)


def main():
    if len(sys.argv) != 2:
        print(ERR_PARAMS)
    canciones_usuarios, canciones_playlist = crear_grafo_desde_tsv(sys.argv[1])
    procesar_entrada(canciones_usuarios, canciones_playlist)


if __name__ == "__main__":
    main()
