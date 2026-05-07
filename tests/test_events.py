import unittest
from src.core.graph import Grafo
from src.core.vertex import Vertice
from src.core.edge import Aresta
from src.service.event_handler import GerenciadorEventos

class TesteEventos(unittest.TestCase):
    def testar_bloqueio_aresta(self):
        """Caso: aplicar acidente bloqueia a aresta."""
        grafo = Grafo(direcionado=True)
        grafo.adicionar_vertice(Vertice(0))
        grafo.adicionar_vertice(Vertice(1))
        grafo.adicionar_aresta(Aresta(0, 1, 5))
        gerenciador = GerenciadorEventos(grafo)
        gerenciador.aplicar_acidente(0, 1)
        self.assertTrue(gerenciador.esta_bloqueada(0, 1))