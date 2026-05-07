class GerenciadorEventos:
    """Gerencia eventos simulados: acidente (bloqueio) e congestionamento (multiplicador)."""

    def __init__(self, grafo):
        self.grafo = grafo
        self.arestas_bloqueadas = set()  # conjunto de tuplas (origem, destino)

    def aplicar_acidente(self, origem: int, destino: int):
        """Bloqueia uma aresta, impedindo sua travessia."""
        self.arestas_bloqueadas.add((origem, destino))

    def aplicar_congestionamento(self, origem: int, destino: int, fator: float):
        """Multiplica o peso da aresta por um fator (ex.: 2.0 para dobrar)."""
        for aresta in self.grafo.obter_adjacentes(origem):
            if aresta.destino == destino:
                aresta.peso *= fator
                break

    def esta_bloqueada(self, origem, destino):
        """Verifica se uma aresta específica está bloqueada."""
        return (origem, destino) in self.arestas_bloqueadas