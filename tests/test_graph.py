import unittest
from src.core.graph import Grafo
from src.core.vertex import Vertice
from src.core.edge import Aresta

class TesteGrafo(unittest.TestCase):
    def setUp(self):
        self.grafo = Grafo(direcionado=True)
        self.vertice_a = Vertice(0, "A")
        self.vertice_b = Vertice(1, "B")
        self.grafo.adicionar_vertice(self.vertice_a)
        self.grafo.adicionar_vertice(self.vertice_b)

    def testar_adicionar_vertice(self):
        """Caso base: adicionar vértice deve aumentar contagem."""
        self.assertEqual(len(self.grafo.vertices), 2)

    def testar_adicionar_aresta(self):
        """Caso base: adicionar aresta e verificar adjacência."""
        aresta = Aresta(0, 1, 10)
        self.grafo.adicionar_aresta(aresta)
        adjacentes = self.grafo.obter_adjacentes(0)
        self.assertEqual(len(adjacentes), 1)
        self.assertEqual(adjacentes[0].peso, 10)

    def testar_adjacencia_vazia(self):
        """Caso grafo sem arestas: adjacência de vértice sem vizinhos é lista vazia."""
        adjacentes = self.grafo.obter_adjacentes(0)
        self.assertEqual(len(adjacentes), 0)