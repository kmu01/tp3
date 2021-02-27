from grafos import Grafo
from errores import *
from collections import deque
from io import StringIO

GRAFO_USUARIOS = 'users'
GRAFO_PLAYLIST = 'playlists'

# Diccionario que tiene las distintas operaciones con el grafo que requieren para operar
COMANDOS = {
    'camino': GRAFO_USUARIOS,
    'mas_importantes': GRAFO_PLAYLIST,
    'recomendacion': GRAFO_USUARIOS,
    'ciclo': GRAFO_PLAYLIST,
    'rango': GRAFO_PLAYLIST,
    'clustering': GRAFO_PLAYLIST
}


# ╔════════════════════════════════════╗
#               COMANDOS
# ╚════════════════════════════════════╝

def camino(canciones, params):
    """
    :param canciones: Grafo bipartito de canciones y usuarios, sus aristas tienen info de playlist.
    :param params: Contiene las canciones de origen y destino en formato "cancion_origen >>>> cancion_final"
    Recorre el grafo desde nuestro origen hasta llegar a nuestro destino, guardando el trayecto que hizo en el camino.
    """
    origen_destino = params.split(' >>>> ')
    if len(origen_destino) != 2:
        print(ERR_FORMATO)
        return
    origen = origen_destino[0]
    destino = origen_destino[1]
    if not canciones.pertenece(origen) or not canciones.pertenece(destino):
        print(ERR_CANCIONES)
        return
    padres, distancia = camino_minimo_bfs(canciones, origen, destino)
    if not padres or not distancia:
        print(ERR_CAMINO)
        return
    imprimir_camino_minimo(canciones, padres, destino)
    return


def mas_importantes(canciones, params):
    """
        :param canciones:
        :param params:
        momento page_rank
    """
    pass


def recomendacion(canciones, params):

    pass


def ciclo(canciones, params):
    """
    :param canciones:
    :param params:
    Seguramente esto es tema de backtracking
    """
    pass

def rango(canciones, params):
    """
    :param canciones:
    :param params:
    Reciclamos camino_minimo_bfs, pero sin especificar destino.
    """
    pass


def clustering(canciones, cancion=None):
    pass


# ╔════════════════════════════════════╗
#         OPERACIONES AUXILIARES
# ╚════════════════════════════════════╝

def camino_minimo_bfs(grafo, origen, destino=None):
    """
    Si hay un destino especificado:
        - Calcula el camino minimo desde el origen al destino, y regresa devuelve padres y distancias
        - Si no existe tal camino devuelve None.
    Si no hay destino especificado:
        - Calcula los caminos minimos de cada vertice al origen, y devuelve padres y distancias
    """
    distancia, padres, visitado = {}, {}, {}
    for v in grafo:
        distancia[v] = float('inf')
    distancia[origen] = 0
    q = deque()
    q.append(origen)
    while q:
        v = q.popleft()
        for w in grafo.adyacentes:
            if v not in visitado:
                distancia[w] += 1
                padres[w] = v
                visitado[w] = True
                q.append(v)
                # Si llegamos a nuestro destino paramos
                if destino and v == destino:
                    return padres, distancia
    if not destino: return padres, distancia
    return None

def imprimir_camino_minimo(canciones, padres, destino):
    """
    Guardamos el camino desde el destino hasta el origen.
    Lo invertimos y luego lo imprimimos siguiendo el formato:
    (cancion) --> aparece en playlist --> (playlist) --> de --> (usuario) --> tiene una playlist --> (playlist) --> donde aparece --> (cancion)
    """
    camino = []
    actual = destino
    while padres[actual]:
        camino.append(actual)
        actual = padres[actual]
    camino.reverse()
    txt = StringIO()
    # Como se recorre: cancion -> usuario -> cancion, la pos de las canciones son pares y la de los usuarios es impar
    # (estoy seguro que hay una forma mas elegante de hacer esto)
    for i in range(len(camino)):
        if i % 2 == 0:
            txt.write(camino[i])
            if camino[i+1]:
                txt.write(' --> ' + 'aparece en playlist' + ' --> ' + canciones.obtener_peso_arista(camino[i], camino[i+1]) + ' --> de --> ')
        else:
            txt.write(camino[i] + ' --> tiene una playlist --> ' + canciones.obtener_peso_arista(camino[i], camino[i+1]) + ' --> donde aparece -->')

    print(txt.getvalue())