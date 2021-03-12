from random import *

# Definimos un Grafo a partir de un diccionario de diccionarios
class Grafo(object):
    def __init__(self, es_dirigido=False):
        """Inicia el grafo"""
        self.vertices = {}
        self.dirigido = es_dirigido

    def agregar_vertice(self, v):
        """Agrega un vertice al grafo"""
        if not v in self.vertices.keys():
            self.vertices[v] = {}

    def borrar_vertice(self, vertice):
        """Elimina el vertice del grafo, junto a todas las uniones que este tenia"""
        for v in self.vertices:
            if v in self.vertices[v].keys():
                del self.vertices[v][vertice]
        del self.vertices[vertice]

    def obtener_vertices(self):
        """Devuelve lista con los vertices del grafo"""
        return list(self.vertices.keys())
    
    def obtener_cantidad_vertices(self):
        """Devuelve la cantidad de vertices del grafo"""
        return len(self.vertices.keys())

    def pertenece(self,v):
        """Comprueba si el vertice esta dentro del grafo"""
        return v in self.vertices.keys()

    def agregar_arista(self, v, w, peso=1):
        """Agrega o actualiza una arista al grafo, si los vertices ingresados existen"""
        if not v in self.vertices or not w in self.vertices:
            return False
        self.vertices[v][w]= peso
        if not self.dirigido: self.vertices[w][v] = peso

    def borrar_aristas(self, v, w):
        """Elimina la arista que conecta los vertices indicados"""
        del self.vertices[v][w]
        if not self.dirigido: del self.vertices[w][v]

    def obtener_peso_arista(self, v, w):
        """Obtiene el peso de la arista entre los dos vertices indicados"""
        return self.vertices[v][w]

    def es_adyacente(self, v, w):
        """Ve si existe una arista entre los vertices indicados"""
        return w in self.vertices[v]

    def adyacentes(self,v):
        """Devuelve una lista con los vertices adyacentes a v"""
        return list(self.vertices[v].keys())

    def crear_iterador(self):
        """Crea un iterados"""
        return iter(self.vertices)
    
    def obtener_vertice_aleatorio (self):
        """Devuelve un vertice de forma aleatoria"""
        return random.choice(list(self.vertices.keys()))
    
    def obtener_adyacente_aleatorio (self,v):
        """Devuelve un vertice adyacente a v de forma aleatoria"""
        return choice(list(self.vertices[v].keys()))