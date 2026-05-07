class Vertice:
    """Representa um vértice (cruzamento) no grafo da malha viária."""

    def __init__(self, identificador: int, nome: str = "", lat: float = 0.0, lon: float = 0.0):
        """
        Parâmetros:
        - identificador: número único do vértice (usado nas arestas e Dijkstra)
        - nome: nome descritivo (ex.: 'Centro', 'Bairro A')
        - lat, lon: coordenadas geográficas para exibição no mapa
        """
        self.id = identificador
        self.nome = nome
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return f"Vertice(id={self.id}, nome='{self.nome}')"

    def __eq__(self, outro):
        if isinstance(outro, Vertice):
            return self.id == outro.id
        return False

    def __hash__(self):
        return hash(self.id)