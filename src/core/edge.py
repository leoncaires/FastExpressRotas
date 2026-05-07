class Aresta:
    """Representa uma aresta direcionada (via) entre dois vértices, com peso (tempo)."""

    def __init__(self, origem: int, destino: int, peso: float):
        """
        - origem: id do vértice de origem
        - destino: id do vértice de destino
        - peso: tempo de percurso em minutos (peso usado no Dijkstra)
        """
        self.origem = origem
        self.destino = destino
        self.peso = peso

    def __repr__(self):
        return f"Aresta({self.origem} -> {self.destino}, peso={self.peso})"