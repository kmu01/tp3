from grafos import Grafo

GRAFO_USUARIOS = 'users'
GRAFO_PLAYLIST = 'playlists'

# Diccionario que tiene las distintas operaciones, con el minimo y maximo de parametros, además del tipo de grafo que requieren
COMANDOS = {
    'camino': (2, 3, GRAFO_USUARIOS),
    'mas_importantes': (1, 2, GRAFO_PLAYLIST),
    'recomendacion': (2, 3, GRAFO_USUARIOS),
    'ciclo': (2, 3, GRAFO_PLAYLIST),
    'rango': (2, 3, GRAFO_PLAYLIST),
    'clustering': (0, 2, GRAFO_PLAYLIST)
}