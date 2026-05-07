import json
from src.core.graph import Grafo
from src.core.vertex import Vertice
from src.core.edge import Aresta

def carregar_grafo_de_json(caminho_arquivo: str) -> Grafo:
    """
    Lê um arquivo JSON no formato definido (com 'vertices' e 'arestas')
    e constrói um grafo direcionado.
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    grafo = Grafo(direcionado=True)

    # Adiciona todos os vértices primeiro
    for v_dados in dados.get("vertices", []):
        vertice = Vertice(
            identificador=v_dados["id"],
            nome=v_dados.get("nome", ""),
            lat=v_dados.get("lat", 0.0),
            lon=v_dados.get("lon", 0.0)
        )
        grafo.adicionar_vertice(vertice)

    # Depois adiciona as arestas
    for a_dados in dados.get("arestas", []):
        aresta = Aresta(
            origem=a_dados["origem"],
            destino=a_dados["destino"],
            peso=a_dados["peso"]
        )
        grafo.adicionar_aresta(aresta)

    return grafo