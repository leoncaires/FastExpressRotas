from .vertex import Vertice
from .edge import Aresta

class Grafo:
    """Grafo direcionado e ponderado, usando lista de adjacência."""

    def __init__(self, direcionado=True):
        self.vertices = {}          # id -> Vertice
        self.lista_adj = {}         # id -> lista de Aresta (arestas que partem do vértice)
        self.direcionado = direcionado

    def adicionar_vertice(self, vertice: Vertice):
        """Adiciona um vértice se ainda não existir, inicializa a lista de adjacência."""
        if vertice.id not in self.vertices:
            self.vertices[vertice.id] = vertice
            self.lista_adj[vertice.id] = []

    def adicionar_aresta(self, aresta: Aresta):
        """
        Adiciona aresta direcionada. Se o grafo for não-direcionado,
        também adiciona a aresta reversa automaticamente.
        """
        if aresta.origem in self.lista_adj and aresta.destino in self.vertices:
            self.lista_adj[aresta.origem].append(aresta)
            if not self.direcionado:
                # Para grafo não direcionado, cria aresta espelhada
                aresta_reversa = Aresta(aresta.destino, aresta.origem, aresta.peso)
                self.lista_adj[aresta.destino].append(aresta_reversa)

    def obter_adjacentes(self, id_vertice: int) -> list:
        """Retorna a lista de arestas que partem do vértice especificado."""
        return self.lista_adj.get(id_vertice, [])

    def obter_vertice(self, id_vertice: int) -> Vertice:
        """Retorna o objeto Vertice pelo id."""
        return self.vertices.get(id_vertice)

    def obter_todos_vertices(self) -> list:
        """Retorna lista de todos os objetos Vertice."""
        return list(self.vertices.values())

    def __str__(self):
        qtd_vertices = len(self.vertices)
        qtd_arestas = sum(len(lista) for lista in self.lista_adj.values())
        return f"Grafo(V={qtd_vertices}, E={qtd_arestas})"