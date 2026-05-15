class Aresta:
    """Representa uma aresta direcionada (via) entre dois vértices, com peso (tempo)."""

    def __init__(self, origem: int, destino: int, peso: float, nome: str = None, geometry: list = None):
        """
        - origem: id do vértice de origem
        - destino: id do vértice de destino
        - peso: tempo de percurso em minutos (peso usado no Dijkstra)
        - nome: nome da rua (opcional)
        - geometry: lista de coordenadas [lat, lon] que descrevem o traçado da via (opcional)
        """
        self.origem = origem
        self.destino = destino
        self.peso = peso
        self.nome = nome
        self.geometry = geometry

    def __repr__(self):
        return f"Aresta({self.origem} -> {self.destino}, peso={self.peso}, nome={self.nome})"