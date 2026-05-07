from src.algorithms.dijkstra import dijkstra, reconstruir_caminho

class ServicoRota:
    """Serviço de aplicação que encapsula o cálculo de rotas usando Dijkstra."""

    def __init__(self, grafo):
        self.grafo = grafo

    def encontrar_caminho_mais_curto(self, id_inicio: int, id_alvo: int):
        """
        Calcula o caminho mais curto entre dois vértices.
        Retorna: (lista de ids do caminho, distância total)
        Se não houver caminho, distância = inf e lista vazia.
        """
        distancias, antecessores = dijkstra(self.grafo, id_inicio, id_alvo)
        caminho = reconstruir_caminho(antecessores, id_inicio, id_alvo)
        distancia = distancias.get(id_alvo, float('inf'))
        return caminho, distancia