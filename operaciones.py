from random import random
from grafos import Grafo
from errores import *
from collections import deque
from io import StringIO
import operator

GRAFO_USUARIOS = 'users'
GRAFO_PLAYLIST = 'playlists'

COEFICIENTE_AMORTIGUACION = 0.85
CANTIDAD_ITERACIONES_PAGERANK = 5

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
    if not canciones.pertenece(origen) or not canciones.pertenece(destino):
        print(ERR_CANCIONES)
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
    i = 0
    w = 0
    while (w < n):
        # Para ver si es una cancion, porque si es un usuario no quiero agregarlo
        if (" - " in pagerank[i][0] and i < n - 1):
            print(pagerank[i][0], end="; ")
            w += 1
        elif (" - " in pagerank[i][0] and i == n-1):
            print(pagerank[i][0])
            w += 1
        i += 1


def recomendacion(canciones, tipo, cantidad, lista_canciones):
    """
    :param canciones: Grafo bipartito de canciones y usuarios, sus aristas tienen info de playlist.
    :param params: usuarios/canciones indicando si se desea una recomendacion de usuarios o canciones,
    n, la cantidad de recomendaciones deseadas y una serie de canciones a partir de las cuales se
    buscan las recomendaciones.
    """
    # Le doy la forma aleatoria a las canciones
    lista_canciones = random.shuffle(lista_canciones.split(" >>>> "))
    pr_personalizado = {}
    for cancion in lista_canciones:
        pagerank_personalizado(canciones, cancion, pr_personalizado)
    pr_ordenado = sorted(pr_personalizado.items(), key=operator.itemgetter(1), reverse=True)
    listado = []
    for elemento in pr_ordenado:
        # Si busco canciones y es una cancion lo agrego. Adevas verifico que no sea una de las pasadas por parametro
        if " - " in elemento[0] and tipo == "canciones" and elemento[0] not in canciones:
            listado.append(elemento[0])
        # Si busco usuarios y  no es una cancion (es usuario) lo agrego
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
    canciones = set()
    canciones.add(origen)
    if not _ciclo(canciones, n, origen, 0, canciones):
        print(ERR_CAMINO)
        return
    for cancion in canciones:
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
    return


def clustering(canciones, cancion=None):
    if not cancion:
        return obtener_clustering_promedio(canciones)
    else:
        obtener_clustering_individual(canciones, cancion)


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
            if camino[i + 1]:
                txt.write(' --> ' + 'aparece en playlist' + ' --> ' + canciones.obtener_peso_arista(camino[i], camino[
                    i + 1]) + ' --> de --> ')
        else:
            txt.write(camino[i] + ' --> tiene una playlist --> ' + canciones.obtener_peso_arista(camino[i], camino[
                i + 1]) + ' --> donde aparece -->')

    print(txt.getvalue())


def _ciclo(grafo, largo, cancion_actual, posicion_actual, canciones):
    """
    Funcion auxiliar que trabaja de forma recursiva. Recibe el largo esperado del ciclo,
    la cancion y posicion actual y las canciones consideradas dentro del ciclo.
    """
    if largo == posicion_actual and canciones[0] == cancion_actual:
        return True
    for cancion in grafo.adyacentes(cancion_actual):
        posicion_actual += 1
        canciones.add(cancion)
        if not es_viable(largo, cancion, posicion_actual, canciones):
            canciones.pop()
            continue
        if _ciclo(grafo, largo, cancion, posicion_actual, canciones):
            return True
    return False


def es_viable(largo, cancion, posicion, canciones):
    if (posicion > largo):  # Poda por si ya me pase del largo pedido
        return False
    if (
            cancion in canciones and posicion != largo):  # Evita que vuelva por una arista de la que vino a no ser que este al final
        return False
    if (largo == posicion and canciones[
        0] != cancion):  # Cuando llego a recorrer las canciones necesarias se fija si es un ciclo
        return False
    return True


def obtener_clustering_promedio(canciones):
    """Devuelve el coeficiente de Clustering promedio entre las canciones"""
    suma = 0
    for v in canciones: suma += obtener_clustering_individual(canciones, v)
    return suma / len(canciones)


def obtener_clustering_individual(canciones, c):
    """Devuelve el coeficiente de Clustering de una canción"""
    if not canciones.pertenece(c):
        print(ERR_CANCIONES)
        return
    cant = 0
    adyacentes = canciones.obtener_adyacentes(c)
    grado_salida = len(adyacentes)
    for v in adyacentes:
        for w in adyacentes:
            if v == w: continue
            if canciones.es_adyacente(v, w): cant += 1
    return cant / ((grado_salida - 1) * grado_salida)


def pagerank(grafo, pagerank):
    """Calcula el pagerank de un grafo. Devuelve un diccionario con cada vertice como clave"""
    cant_vertices = grafo.obtener_cantidad_vertices()
    for vertice in canciones.obtener_vertices():
        pagerank[vertice] = 1 / cant_vertices
    for i in range(CANTIDAD_ITERACIONES_PAGERANK):
        for vertice in random.shuffle(grafo.obtener_vertices()):
            valor = pagerank_vertice(grafo, vertice, pagerank, cant_vertices)
            pagerank[valor] = valor
    pagerank_ordenado = sorted(pagerank.items(), key=operator.itemgetter(1), reverse=True)
    return pagerank_ordenado


def pagerank_vertice(grafo, vertice, valores, n):
    """Calcula el valor de pagerank especifico para un vertice de un grafo"""
    sumatoria = 0
    for adyacente in grafo.obtener_adyacentes(vertice):
        sumatoria += (valores[adyacente]) / len(grafo.obtener_adyacentes(adyacente))
    valor = ((1 - COEFICIENTE_AMORTIGUACION) / n) + (COEFICIENTE_AMORTIGUACION * sumatoria)
    return valor


def pagerank_personalizado(grafo, vertice, pr_personalizado):
    visitados = set()
    visitados.add(vertice)
    _pagerank_personalizado(grafo, vertice, pr_personalizado, visitados)


def _pagerank_personalizado(grafo, v, pr_personalizado, visitados):
    if (len(visitados) == grafo.cant_vertices()):
        return
    actual = grafo.obtener_adyacente_aleatorio(v)
    cant_adyacentes = len(grafo.adyacentes(v))
    pr_personalizado[actual] = (pr_personalizado[v] / cant_adyacentes)
    if (actual not in visitados):
        visitados.add(actual)
    _pagerank_personalizado(grafo, actual, tipo, cant, pr_personalizado, visitados)