from random import shuffle
from grafos import Grafo
from errores import *
from collections import deque
from io import StringIO
import operator

GRAFO_USUARIOS = 'users'
GRAFO_PLAYLIST = 'playlists'

COEFICIENTE_AMORTIGUACION = 0.85
CANTIDAD_ITERACIONES_PAGERANK = 40
LARGO_PR_PERSONALIZADO = 100

# Operaciones
CMD_CAMINOS = 'camino'
CMD_IMPORTANTES = 'mas_importantes'
CMD_RECOMENDS = 'recomendacion'
CMD_CICLO = 'ciclo'
CMD_RANGO = 'rango'
CMD_CLUSTER = 'clustering'


# ╔════════════════════════════════════╗
#               COMANDOS
# ╚════════════════════════════════════╝

def camino(canciones, origen, destino):
    """
    :param canciones: Grafo bipartito de canciones y usuarios, sus aristas tienen info de playlist.
    :param origen: Canción donde empieza.
    :param destino: Canción donde termina.
    Recorre el grafo desde nuestro origen hasta llegar a nuestro destino, guardando el trayecto que hizo en el camino.
    """
    if (" - " not in origen) or (" - " not in destino):
        print (ERR_ORIGEN_DEST)
        return
    if (not canciones.pertenece(origen)) or (not canciones.pertenece(destino)):
        print(ERR_ORIGEN_DEST)
        return
    padres, distancia = camino_minimo_bfs(canciones, origen, destino)
    if not padres or not distancia:
        print(ERR_CAMINO)
        return
    imprimir_camino_minimo(canciones, padres, destino)
    return


def mas_importantes(canciones, n, PR):
    """
    :param canciones: Grafo bipartito de canciones y usuarios, sus aristas tienen info de playlist.
    :param n: Numero de canciones que se desea mostrar.
    Se buscan e imprimen las n canciones mas importantes del grafo
    """
    if len(PR.keys()) == 0:
        pagerank(canciones, PR)
    pr_ordenado = sorted(PR.items(), key=operator.itemgetter(1), reverse=True)
    i = 0
    w = 0
    while (w < n):
        if (' - ' in pr_ordenado[i][0] and w < n - 1):
            print(pr_ordenado[i][0], end="; ")
            w += 1
        elif (' - ' in pr_ordenado[i][0] and w == n-1):
            print(pr_ordenado[i][0])
            w += 1
        i += 1


def recomendacion(canciones, tipo, cantidad, lista_canciones):
    """
    :param canciones: Grafo bipartito de canciones y usuarios, sus aristas tienen info de playlist.
    :param params: usuarios/canciones indicando si se desea una recomendacion de usuarios o canciones,
    n, la cantidad de recomendaciones deseadas y una serie de canciones a partir de las cuales se
    buscan las recomendaciones.
    Genera una cantidad deseada de recomendaciones de usuarios o de canciones a partir de una serie
    de canciones pasadas por parámetro haciendo uso del algoritmo de PageRank Personalizado.
    """
    lista_canciones = lista_canciones.split(" >>>> ")
    shuffle (lista_canciones)
    sumas = {}
    for cancion in lista_canciones:
        pagerank_personalizado(canciones, cancion, 1, sumas, 0)
    pr_ordenado = sorted(sumas.items(), key=operator.itemgetter(1), reverse=True)
    listado = []
    for elemento in pr_ordenado:
        if " - " in elemento[0] and tipo == "canciones" and elemento[0] not in lista_canciones:
            listado.append(elemento[0])
        elif " - " not in elemento[0] and tipo == "usuarios":
            listado.append(elemento[0])
    for i in range(cantidad):
        if (i < cantidad - 1):
            print(listado[i], end='; ')
        else:
            print(listado[i])
    return


def ciclo(canciones, n, origen):
    """
    :param canciones:Grafo no dirigido que relaciona canciónes que comparten playlists.
    :param n: El largo elegido para el ciclo.
    :param origen: La cancion por la que comienza el ciclo.
    Recorre el grafo desde la cancion de origen utilizando backtracking hasta generar un ciclo
    de n canciones.
    """
    listado_canciones = []
    if not _ciclo(canciones, n, origen, 0, listado_canciones):
        print(ERR_CAMINO)
        return
    for cancion in listado_canciones:
        print(cancion, end=' --> ')
    print(origen)
    return


def rango(canciones, n, origen):
    """
    :param canciones: Grafo no dirigido que relaciona canciónes que comparten playlists
    :param params: La cancion origen para la busqueda y el rango o distancia n que se busca
    Se busca determinar la cantidad de canciones que se encuentran a una distancia n de la canción de origen
    Se imprime por pantalla dicha cantidad, pudiendo ser esta 0.
    """
    padres, distancias = camino_minimo_bfs(canciones, origen)
    contador = 0
    for cancion in distancias:
        if distancias[cancion] == n:
            contador += 1
    print(contador)


def clustering(canciones, cancion=None):
    if not cancion:
        print (obtener_clustering_promedio(canciones))
    else:
        print (obtener_clustering_individual(canciones, cancion))


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
    for v in grafo.obtener_vertices():
        distancia[v] = float('inf')
    distancia[origen] = 0
    padres[origen] = None
    visitado[origen] = True
    q = deque()
    q.append(origen)
    while q:
        v = q.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitado.keys():
                distancia[w] = distancia [v] + 1
                padres[w] = v
                visitado[w] = True
                q.append(w)
            if destino and w == destino:
                return padres, distancia
    if not destino: return padres, distancia
    return None, None


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
    camino.append(actual)
    camino.reverse()
    txt = StringIO()
    for i in range(len(camino)-1):
        if i % 2 == 0:
            txt.write(camino[i])
            txt.write(' --> ' + 'aparece en playlist' + ' --> ' + canciones.obtener_peso_arista(camino[i], camino[
                i + 1]) + ' --> de --> ')
        else:
            txt.write(camino[i] + ' --> tiene una playlist --> ' + canciones.obtener_peso_arista(camino[i], camino[
                i + 1]) + ' --> donde aparece -->')
    txt.write (' ' + camino[len(camino)-1])
    print(txt.getvalue())


def _ciclo(grafo, largo, cancion_actual, posicion_actual, canciones):
    """
    Funcion auxiliar que trabaja de forma recursiva. Recibe el largo esperado del ciclo,
    la cancion y posicion actual y las canciones consideradas dentro del ciclo.
    """
    if largo == posicion_actual and canciones[0] == cancion_actual:
        return True
    canciones.append(cancion_actual)
    for cancion in grafo.adyacentes(cancion_actual):
        if not es_viable(largo, cancion, posicion_actual+1, canciones):            
            continue
        if _ciclo(grafo, largo, cancion, posicion_actual+1, canciones):
            return True
    canciones.pop()
    return False


def es_viable(largo, cancion, posicion, canciones):
    """
    Funcion auxiliar para el calculo de un ciclo que verifica si una solucion parcial es viable
    """
    if (posicion > largo):
        return False
    if (cancion in canciones and posicion != largo):
        return False
    if (largo == posicion and canciones[
        0] != cancion):
        return False
    return True


def obtener_clustering_promedio(grafo):
    """
    Devuelve el coeficiente de Clustering promedio entre las canciones
    """
    suma = 0
    canciones = grafo.obtener_vertices()
    cant_vertices = grafo.obtener_cantidad_vertices()
    for v in canciones: suma += obtener_clustering_individual(grafo, v)
    return (suma / cant_vertices)


def obtener_clustering_individual(canciones, c):
    """
    Devuelve el coeficiente de Clustering de una canción
    """
    if not canciones.pertenece(c):
        print(ERR_CANCIONES)
        return
    cant = 0
    adyacentes = canciones.adyacentes(c)
    grado_salida = len(adyacentes)
    if (grado_salida < 2):
        return 0
    for v in adyacentes:
        for w in adyacentes:
            if v == w: continue
            if canciones.es_adyacente(v, w): cant += 1
    return cant / ((grado_salida - 1) * grado_salida)


def pagerank(grafo, PR):
    """
    Calcula el pagerank de un grafo
    """
    cant_vertices = grafo.obtener_cantidad_vertices()
    for vertice in grafo.obtener_vertices():
        PR[vertice] = 1 / cant_vertices
    for i in range(CANTIDAD_ITERACIONES_PAGERANK):
        vertices = grafo.obtener_vertices()
        shuffle(vertices)
        for vertice in vertices:
            PR[vertice] = pagerank_vertice(grafo, vertice, PR, cant_vertices)
    return


def pagerank_vertice(grafo, vertice, PR, n):
    """
    Calcula el valor de pagerank especifico para un vertice de un grafo
    """
    sumatoria = 0
    for adyacente in grafo.adyacentes(vertice):
        sumatoria += (PR[adyacente]) / len(grafo.adyacentes(adyacente))
    valor = ((1 - COEFICIENTE_AMORTIGUACION) / n) + (COEFICIENTE_AMORTIGUACION * sumatoria)
    return valor


def pagerank_personalizado(grafo, v, valor, suma,n):
    """
    Calcula de forma recursiva el PageRank Personalizado hasta llegar a un largo predefinido
    """
    if (n == LARGO_PR_PERSONALIZADO):
        return
    actual = grafo.obtener_adyacente_aleatorio(v)
    cant_adyacentes = len(grafo.adyacentes(v))
    nuevo_valor = (valor/ cant_adyacentes)
    if (not actual in suma.keys()):
        suma[actual] = nuevo_valor
    else:
        suma[actual] += nuevo_valor
    pagerank_personalizado(grafo, actual, nuevo_valor, suma, n+1)