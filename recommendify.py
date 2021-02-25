import sys
import csv
import operaciones as op
from grafos import Grafo

"""Seguramente queremos poner estas constantes en otro archivo"""

# Constantes varias
MIN = 0
MAX = 1

# Mensajes de error
ERR_PARAMS = "Cantidad de parametros incorrecta"
ERR_CMD = "El comando no existe o esta mal escrito"




def crear_grafo_desde_tsv(ruta):
    """
    Si existe, abre un tsv para cargar su información al Grafo de la siguiente forma:
    Nuestros campos son: ID    USER_ID	TRACK_NAME	ARTIST	PLAYLIST_ID PLAYLIST_NAME	GENRES
    Crea un vértice (v1) con el USER_ID
    Crea otro vértice (v2) como TRACK_NAME - ARTIST
    Une ambos vertices con una arista que de peso (p) tiene la playlist como una tupla (PLAYLIST_ID, PLAYLIST_NAME)
    """
    grafo = Grafo()
    with open(ruta) as archivo_tsv:
        # Mira si la primer linea es un encabezado, de ser así la ignora.
        tiene_encabezado = csv.Sniffer().has_header(archivo_tsv.read(1024))
        archivo_tsv.seek(0)  # Volver al comienzo del archivo.
        lector = csv.reader(archivo_tsv, delimiter="\t")
        if tiene_encabezado:
            next(lector)
        for fila in lector:
            v1 = fila[1]
            v2 = fila[2] + ' - ' + fila[3]
            p = (fila[4], fila[5])
            grafo.agregar_vertice(v1)
            grafo.agregar_vertice(v2)
            grafo.agregar_arista(v1, v2, p)
    return grafo


def procesar_comandos(comando, parametros, grafo):
    """
    Comprueba si los comandos existen y estan bien escritos.
    Si lo estan, ejecuta el comando enviado.
    Si no, devuelve error.
    """
    if comando not in op.COMANDOS:
        print(ERR_CMD)
        return
    cant_params = op.COMANDOS.get(comando)
    if len(parametros) not in range(cant_params[MIN],cant_params[MAX]):
        print(ERR_PARAMS)
        return
    getattr(op, comando)(grafo, *parametros)


def procesar_entrada(grafo):
    """Separa la entrada en el comando y sus respectivos parametros, luego los procesa"""
    for linea in sys.stdin:
        parse = linea.split()
        if len(parse) > 0:
            comando = parse[0]
            parametros = []
            if len(parse) > 1:
                parametros = parse[1:]
            procesar_comandos(comando, parametros, grafo)
        else:
            print(ERR_CMD)


def main():
    if len(sys.argv) != 2:
        print(ERR_PARAMS)
    grafo = crear_grafo_desde_tsv(sys.argv[1])
    procesar_entrada(grafo)


if __name__ == "__main__":
    main()
