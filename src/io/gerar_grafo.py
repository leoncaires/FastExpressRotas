import osmnx as ox
from shapely.geometry import LineString
import json
import os

# Coordenadas da Praça da Sé, São Paulo
latitude = -23.5505
longitude = -46.6333
distancia = 1200  # metros

print(f"Baixando grafo ao redor da Praça da Sé (lat={latitude}, lon={longitude}, raio={distancia}m)...")
grafo_ox = ox.graph_from_point(
    (latitude, longitude),
    dist=distancia,
    dist_type='bbox',
    network_type='drive'   # simplify=True (padrão)
)

vertices = []
arestas = []

# 1. Mapeamento auxiliar: node -> ruas incidentes (para nomes de esquina)
node_to_streets = {}
for u, v, key, data in grafo_ox.edges(keys=True, data=True):
    street = data.get('name', None)
    if isinstance(street, list):
        street = street[0]
    if not street:
        continue
    node_to_streets.setdefault(u, set()).add(street)
    node_to_streets.setdefault(v, set()).add(street)

# 2. Gerar vértices com nomes únicos
for node in grafo_ox.nodes():
    data = grafo_ox.nodes[node]
    lat = data['y']
    lon = data['x']

    nome_proprio = data.get('name', None)
    ruas = node_to_streets.get(node, set())

    if nome_proprio:
        nome = nome_proprio
    elif len(ruas) >= 2:
        ruas_ordenadas = sorted(ruas)
        nome = f"{ruas_ordenadas[0]} c/ {ruas_ordenadas[1]}"
    elif len(ruas) == 1:
        nome = list(ruas)[0]
    else:
        nome = f"Ponto {node}"

    vertices.append({
        "id": node,
        "nome": nome,
        "lat": lat,
        "lon": lon
    })

# 3. Arestas com geometria e nome
for u, v, key, data in grafo_ox.edges(keys=True, data=True):
    length = data.get('length', 100)
    speed_kmh = 30
    tempo_min = (length / 1000) / speed_kmh * 60
    peso = round(tempo_min, 2)

    street = data.get('name', None)
    if isinstance(street, list):
        street = street[0]
    nome_aresta = street if street else f"Via {u}→{v}"

    # Trata geometria como LineString (Shapely) ou lista
    geom = data.get('geometry', None)
    if geom is None:
        # Fallback: linha reta entre os nós
        no_u = grafo_ox.nodes[u]
        no_v = grafo_ox.nodes[v]
        coords = [[no_u['y'], no_u['x']], [no_v['y'], no_v['x']]]
    elif isinstance(geom, LineString):
        # Converte LineString para lista de [lat, lon]
        coords = [[lat, lon] for lon, lat in geom.coords]
    else:
        # Caso venha como lista de tuplas (modos antigos)
        coords = [[lat, lon] for lon, lat in geom]

    # Adiciona a aresta original
    arestas.append({
        "origem": u,
        "destino": v,
        "peso": peso,
        "nome": nome_aresta,
        "geometry": coords
    })

    # Adiciona a aresta reversa (mesmo peso e geometria invertida)
    arestas.append({
    "origem": u,
    "destino": v,
    "peso": peso,
    "nome": nome_aresta,
    "geometry": coords
})

dataset = {"vertices": vertices, "arestas": arestas}

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