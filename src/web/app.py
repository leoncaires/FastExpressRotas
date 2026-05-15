import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import requests
from src.io.file_reader import carregar_grafo_de_json
from src.service.route_service import ServicoRota
from src.service.traffic_simulator import SimuladorTransito

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')

# Carrega o grafo padrão ao iniciar o servidor
caminho_dados = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'malha_exemplo.json')
grafo = carregar_grafo_de_json(caminho_dados)
servico_rota = ServicoRota(grafo)

# Função chamada pelo simulador quando o trânsito muda
def notificar_evento_transito(mensagem):
    print(f"Evento de trânsito: {mensagem}")
    socketio.emit('traffic_event', {'mensagem': mensagem})

# Instancia o simulador (a thread será iniciada apenas no main)
simulador = SimuladorTransito(grafo, notificar_evento_transito)

# -- Rotas --
@app.route('/')
def indice():
    vertices = [{"id": v.id, "nome": v.nome} for v in grafo.obter_todos_vertices()]
    vertices.sort(key=lambda x: x['nome'].lower())
    return render_template('index.html', vertices=vertices)

@app.route('/api/vertices', methods=['GET'])
def obter_vertices():
    vertices = [{"id": v.id, "nome": v.nome, "lat": v.lat, "lon": v.lon}
                for v in grafo.obter_todos_vertices()]
    return jsonify(vertices)

@app.route('/api/rota', methods=['POST'])
def calcular_rota():
    dados = request.get_json()
    id_inicio = int(dados['start'])
    id_alvo = int(dados['target'])

    caminho, distancia = servico_rota.encontrar_caminho_mais_curto(id_inicio, id_alvo)

    # Se o caminho estiver vazio, não há rota disponível
    if not caminho:
        return jsonify({
            "path": [],
            "distance": None,
            "has_path": False,
            "ruas": []
        })

    detalhes_caminho = []
    ruas_percurso = []

    # Adiciona o ponto inicial manualmente
    primeiro = grafo.obter_vertice(caminho[0])
    detalhes_caminho.append({
        "id": caminho[0],
        "nome": primeiro.nome,
        "lat": primeiro.lat,
        "lon": primeiro.lon
    })

    for i in range(1, len(caminho)):
        origem = caminho[i-1]
        destino = caminho[i]
        arestas = grafo.obter_adjacentes(origem)
        nome_rua = None
        geometria = None
        for aresta in arestas:
            if aresta.destino == destino:
                nome_rua = aresta.nome
                geometria = aresta.geometry
                break
        ruas_percurso.append(nome_rua if nome_rua else f"Via {origem}→{destino}")
        
        if geometria:
            for coord in geometria:
                detalhes_caminho.append({
                    "lat": coord[0],
                    "lon": coord[1],
                    "nome": None
                })
        else:
            v_destino = grafo.obter_vertice(destino)
            detalhes_caminho.append({
                "id": destino,
                "nome": v_destino.nome,
                "lat": v_destino.lat,
                "lon": v_destino.lon
            })

    return jsonify({
        "path": detalhes_caminho,
        "distance": distancia if distancia != float('inf') else None,
        "has_path": distancia != float('inf'),
        "ruas": ruas_percurso
    })

@app.route('/api/rota_real', methods=['POST'])
def calcular_rota_real():
    dados = request.get_json()

    inicio = grafo.obter_vertice(int(dados['start']))
    destino = grafo.obter_vertice(int(dados['target']))

    url = f"https://router.project-osrm.org/route/v1/driving/{inicio.lon},{inicio.lat};{destino.lon},{destino.lat}?overview=full&geometries=geojson"

    resposta = requests.get(url)

    if resposta.status_code != 200:
        return jsonify({"erro": "Falha ao consultar API de rotas"}), 500

    resultado = resposta.json()
    rota = resultado['routes'][0]
    coordenadas = rota['geometry']['coordinates']

    caminho_formatado = [
        {"lat": coord[1], "lon": coord[0]}
        for coord in coordenadas
    ]

    distancia_km = round(rota['distance'] / 1000, 2)
    duracao_min = round(rota['duration'] / 60, 1)

    return jsonify({
        "path": caminho_formatado,
        "distance_km": distancia_km,
        "duration_min": duracao_min,
        "origem": inicio.nome,
        "destino": destino.nome
    })

@app.route('/api/simular_evento', methods=['POST'])
def simular_evento():
    dados = request.get_json()
    id_origem = int(dados['origem'])
    id_destino = int(dados['destino'])
    tipo = dados.get('tipo', 'congestionamento')
    fator = float(dados.get('fator', 10.0))   # fator padrão maior

    # Calcula a rota atual para obter todas as arestas
    caminho, _ = servico_rota.encontrar_caminho_mais_curto(id_origem, id_destino)
    if len(caminho) < 2:
        return jsonify({"erro": "Rota não encontrada ou rota com apenas um ponto."}), 400

    # Localiza a aresta de maior peso no caminho
    maior_peso = -1
    aresta_escolhida = None
    for i in range(len(caminho) - 1):
        u = caminho[i]
        v = caminho[i+1]
        arestas = grafo.obter_adjacentes(u)
        for aresta in arestas:
            if aresta.destino == v and aresta.peso > maior_peso:
                maior_peso = aresta.peso
                aresta_escolhida = (u, v)

    if not aresta_escolhida:
        return jsonify({"erro": "Nenhuma aresta encontrada."}), 400

    u, v = aresta_escolhida
    mensagem = simulador.aplicar_evento_manual(u, v, tipo, fator)
    return jsonify({"mensagem": mensagem})

if __name__ == '__main__':
    simulador.iniciar()
    socketio.run(app, debug=False)