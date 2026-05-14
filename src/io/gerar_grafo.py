import osmnx as ox
import json
import os

# Coordenadas da Praça da Sé, São Paulo
latitude = -23.5505
longitude = -46.6333
distancia = 800  # metros (mais ruas, ainda central)

print(f"Baixando grafo ao redor da Praça da Sé (lat={latitude}, lon={longitude}, raio={distancia}m)...")
grafo_ox = ox.graph_from_point(
    (latitude, longitude),
    dist=distancia,
    dist_type='bbox',
    network_type='drive'
)

vertices = []
arestas = []

# Mapeamento auxiliar: node -> rua principal (a mais frequente nas arestas incidentes)
node_to_best_street = {}
for u, v, key, data in grafo_ox.edges(keys=True, data=True):
    street = data.get('name', None)
    if isinstance(street, list):
        street = street[0]
    if not street:
        continue
    # Para cada nó, guardamos a rua (a primeira que aparecer já serve, mas vamos pegar a mais comum)
    for node in (u, v):
        if node not in node_to_best_street:
            node_to_best_street[node] = street
        # podemos trocar se quisermos, mas manter a primeira já resolve

# Agora gera os vértices com nomes legíveis
for node in grafo_ox.nodes():
    data = grafo_ox.nodes[node]
    lat = data['y']
    lon = data['x']

    # 1. Nome próprio do nó (praças, pontos de referência)
    nome = data.get('name', None)

    if not nome:
        # 2. Usa a rua principal associada ao nó (se houver)
        nome = node_to_best_street.get(node, None)

    if not nome:
        # 3. Último recurso: busca nas arestas diretamente
        for _, v, k, edge_data in grafo_ox.edges(node, keys=True, data=True):
            rua = edge_data.get('name', None)
            if isinstance(rua, list):
                rua = rua[0]
            if rua:
                nome = rua
                break
        if not nome:
            for u, _, k, edge_data in grafo_ox.in_edges(node, keys=True, data=True):
                rua = edge_data.get('name', None)
                if isinstance(rua, list):
                    rua = rua[0]
                if rua:
                    nome = rua
                    break

    if not nome:
        # Se ainda não tiver, mantém o ID mas como "Rua (ID)" – bem raro acontecer
        nome = f"Rua {node}"

    vertices.append({
        "id": node,
        "nome": nome,
        "lat": lat,
        "lon": lon
    })

# Arestas: agora também guardamos o nome da rua (se disponível) no atributo "nome"
for u, v, key, data in grafo_ox.edges(keys=True, data=True):
    length = data.get('length', 100)
    speed_kmh = 30
    tempo_min = (length / 1000) / speed_kmh * 60
    peso = round(tempo_min, 2)

    street = data.get('name', None)
    if isinstance(street, list):
        street = street[0]
    nome_aresta = street if street else f"Via {u}→{v}"

    arestas.append({
        "origem": u,
        "destino": v,
        "peso": peso,
        "nome": nome_aresta
    })

dataset = {"vertices": vertices, "arestas": arestas}

# Salva em data/malha_exemplo.json
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
caminho_data = os.path.join(raiz_projeto, "data")
os.makedirs(caminho_data, exist_ok=True)

caminho_arquivo = os.path.join(caminho_data, "malha_exemplo.json")
with open(caminho_arquivo, "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print(f"✅ Grafo gerado com sucesso!")
print(f"   Vértices: {len(vertices)}")
print(f"   Arestas:  {len(arestas)}")
print(f"   Arquivo:  {caminho_arquivo}")