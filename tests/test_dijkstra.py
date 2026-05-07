import unittest
from src.core.graph import Grafo
from src.core.vertex import Vertice
from src.core.edge import Aresta
from src.algorithms.dijkstra import dijkstra, reconstruir_caminho

class TesteDijkstra(unittest.TestCase):
    def criar_grafo_teste(self):
        """Monta um grafo com 4 vértices e arestas específicas para teste."""
        grafo = Grafo(direcionado=True)
        for i in range(4):
            grafo.adicionar_vertice(Vertice(i, f"V{i}"))
        # Estrutura: 0→1(2), 0→2(6), 1→2(3), 2→3(1), 1→3(5)
        grafo.adicionar_aresta(Aresta(0, 1, 2))
        grafo.adicionar_aresta(Aresta(0, 2, 6))
        grafo.adicionar_aresta(Aresta(1, 2, 3))
        grafo.adicionar_aresta(Aresta(2, 3, 1))
        grafo.adicionar_aresta(Aresta(1, 3, 5))
        return grafo

    def testar_caso_base(self):
        """Caso base: caminho mais curto de 0 a 3 é 0→1→2→3 com custo 6."""
        grafo = self.criar_grafo_teste()
        dist, pred = dijkstra(grafo, 0, 3)
        self.assertEqual(dist[3], 6)
        caminho = reconstruir_caminho(pred, 0, 3)
        self.assertEqual(caminho, [0, 1, 2, 3])

    def testar_grafo_vazio(self):
        """Caso grafo vazio: Dijkstra deve retornar distâncias vazias."""
        grafo = Grafo()
        dist, pred = dijkstra(grafo, 0)
        self.assertEqual(dist, {})

    def testar_grafo_completo(self):
        """Caso grafo completo: todos os vértices conectados entre si com peso 1."""
        grafo = Grafo(direcionado=True)
        for i in range(3):
            grafo.adicionar_vertice(Vertice(i))
        for i in range(3):
            for j in range(3):
                if i != j:
                    grafo.adicionar_aresta(Aresta(i, j, 1))
        dist, pred = dijkstra(grafo, 0, 2)
        self.assertEqual(dist[2], 1)
        caminho = reconstruir_caminho(pred, 0, 2)
        self.assertEqual(caminho, [0, 2])