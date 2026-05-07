import heapq

def dijkstra(grafo, id_inicio, id_alvo=None):
    """
    Algoritmo de Dijkstra com fila de prioridade (min-heap).

    Retorna:
    - distancias: dict vértice -> distância mínima desde o início
    - antecessores: dict vértice -> vértice antecessor no caminho mínimo

    Se id_alvo for informado, a execução para ao alcançá-lo (otimização).
    """
    distancias = {v: float('inf') for v in grafo.vertices}
    antecessores = {v: None for v in grafo.vertices}
    distancias[id_inicio] = 0

    # Heap de tuplas (distância acumulada, vértice)
    fila_prioridade = [(0, id_inicio)]

    while fila_prioridade:
        dist_atual, id_atual = heapq.heappop(fila_prioridade)

        # Ignora entradas antigas na heap (lazy deletion)
        if dist_atual > distancias[id_atual]:
            continue

        # Parada antecipada quando o destino é alcançado
        if id_alvo is not None and id_atual == id_alvo:
            break

        # Explora as arestas vizinhas
        for aresta in grafo.obter_adjacentes(id_atual):
            nova_dist = dist_atual + aresta.peso
            if nova_dist < distancias[aresta.destino]:
                distancias[aresta.destino] = nova_dist
                antecessores[aresta.destino] = id_atual
                heapq.heappush(fila_prioridade, (nova_dist, aresta.destino))

    return distancias, antecessores


def reconstruir_caminho(antecessores, id_inicio, id_alvo):
    """Reconstrói o caminho (sequência de vértices) a partir do dicionário de antecessores."""
    caminho = []
    atual = id_alvo
    # Parte do destino e segue os antecessores até a origem
    while atual is not None:
        caminho.append(atual)
        atual = antecessores[atual]
    caminho.reverse()
    # Se o primeiro elemento for a origem, o caminho é válido
    if caminho and caminho[0] == id_inicio:
        return caminho
    else:
        return []   # destino inalcançável