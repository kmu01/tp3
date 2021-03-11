import sys
import csv
import operaciones as op
from errores import *
from grafos import Grafo


def guardar_datos_de_tsv(ruta):
    """
    Si existe, abre un tsv para cargar su información a una matriz:
    Nuestros campos son: ID    USER_ID	TRACK_NAME	ARTIST	PLAYLIST_ID PLAYLIST_NAME	GENRES
    """
    with open(ruta) as archivo_tsv:
        # Mira si la primer linea es un encabezado, de ser así la ignora.
        tiene_encabezado = csv.Sniffer().has_header(archivo_tsv.read(1024))
        archivo_tsv.seek(0)  # Volver al comienzo del archivo.
        lector = csv.reader(archivo_tsv, delimiter="\t")
        datos = []
        if tiene_encabezado:
            next(lector)
        for fila in lector:
            datos.append(fila);
    return datos

def cargar_grafo_usuarios(datos, canciones_usuarios):
    """
    Crea un vértice (v) con el USER_ID
    Crea otro vértice (w) como TRACK_NAME - ARTIST
    Une ambos vertices con una arista que de peso (p) tiene PLAYLIST_NAME
    """
    for fila in datos:
        v = fila[1]
        w = fila[2] + ' - ' + fila[3]
        p = fila[5]
        canciones_usuarios.agregar_vertice(v)
        canciones_usuarios.agregar_vertice(w)
        canciones_usuarios.agregar_arista(v, w, p)

def cargar_grafo_playlist(datos, canciones_playlist):
    """
    Crea un vértice (v) como TRACK_NAME - ARTIST
    Crea aristas entre este vértice y todos los demás que compartan playlist, sin peso
    """
    playlist_actual = None
    comparten_playlist = []
    for fila in datos:
        v = fila[2] + ' - ' + fila[3]
        if playlist_actual == fila[4]:
            comparten_playlist.append(v)
        else:
            playlist_actual = fila[4]
            comparten_playlist = []
        canciones_playlist.agregar_vertice(v)
        for i in comparten_playlist:
            canciones_playlist.agregar_arista(comparten_playlist[i], v)

def procesar_comandos(datos, cmd, params, canciones_usuarios, canciones_playlist, pagerank):
    """
    Comprueba si los comandos existen.
    Si lo estan, ejecuta el comando enviado, dandole los parametros y el grafo que les corresponda.
    Si no, devuelve error.
    """
    if cmd == op.CMD_CAMINOS:
        origen_destino = params.split(' >>>> ')
        if len(origen_destino) != 2:
            print(ERR_FORMATO)
            return
        if canciones_usuarios.obtener_cantidad_vertices() == 0:
            cargar_grafo_usuarios(datos, canciones_usuarios)
        op.camino(canciones_usuarios, origen_destino[0], origen_destino[1])

    elif cmd == op.CMD_IMPORTANTES:
        if canciones_usuarios.obtener_cantidad_vertices() == 0:
            cargar_grafo_usuarios(datos, canciones_usuarios)
        op.mas_importantes(canciones_usuarios, int(params[0]), pagerank)

    elif cmd == op.CMD_RECOMENDS:
        parametros = params.split(' ', 2)
        if len(parametros) != 3:
            print(ERR_FORMATO)
            return
        if canciones_usuarios.obtener_cantidad_vertices() == 0:
            cargar_grafo_usuarios(datos, canciones_usuarios)
        op.recomendacion(canciones_usuarios, parametros[0], int(parametros[1]), parametros[2])

    elif cmd == op.CMD_CICLO:
        n_origen = params.split(' ')
        if len(n_origen) != 2:
            print(ERR_FORMATO)
            return
        if canciones_usuarios.obtener_cantidad_vertices() == 0:
            cargar_grafo_playlist(datos, canciones_playlist)
        op.ciclo(canciones_playlist, int(n_origen[0]), n_origen[1])

    elif cmd == op.CMD_RANGO:
        n_origen = params.split(' ')
        if len(n_origen) != 2:
            print(ERR_FORMATO)
            return
        if canciones_usuarios.obtener_cantidad_vertices() == 0:
            cargar_grafo_playlist(datos, canciones_playlist)
        op.rango(canciones_playlist, int(n_origen[0]), n_origen[1])

    elif cmd == op.CMD_CLUSTER:
        if canciones_usuarios.obtener_cantidad_vertices() == 0:
            cargar_grafo_playlist(datos, canciones_playlist)
        op.clustering(canciones_playlist, params)

    else:
        print(ERR_CMD)
        return


def procesar_entrada(datos, canciones_usuarios, canciones_playlist, pagerank):
    """Separa la entrada en el comando y sus respectivos parametros, luego los procesa"""
    for linea in sys.stdin:
        parse = linea.split()
        if len(parse) > 0:
            comando = parse[0]
            parametros = None
            if len(parse) > 1:
                parametros = ' '.join(parse[1:])
            procesar_comandos(datos, comando, parametros, canciones_usuarios, canciones_playlist, pagerank)
        else:
            print(ERR_CMD)


def main():
    if len(sys.argv) != 2:
        print(ERR_PARAMS)
    canciones_usuarios, canciones_playlist = Grafo()
    pagerank = {}
    datos = guardar_datos_de_tsv(sys.argv[1])
    procesar_entrada(datos, canciones_usuarios, canciones_playlist, pagerank)


if __name__ == "__main__":
    main()
