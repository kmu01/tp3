import sys
import csv
from grafos import Grafo


def crear_grafo_desde_tsv():
    grafo = Grafo()
    with open("example.tsv") as archivo_tsv:
        lector_tsv = csv.reader(archivo_tsv, delimiter="\t")

    return grafo;

def procesar_comandos(comando, parametros, grafo):
    pass

def procesar_entrada(grafo):
    pass


def main():
    if len(sys.argv) != 2:
        print("Cantidad de parametros incorrecta")
    grafo = crear_grafo_desde_tsv(sys.arv[1])
    procesar_entrada(grafo)

if __name__ == "__main__":
    main()