import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
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

# Inicia o simulador de trânsito (thread separada)
simulador = SimuladorTransito(grafo, notificar_evento_transito)
simulador.iniciar()

# -- Rotas --
@app.route('/')
def indice():
    vertices = [{"id": v.id, "nome": v.nome} for v in grafo.obter_todos_vertices()]
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

    detalhes_caminho = []
    for id_v in caminho:
        vertice = grafo.obter_vertice(id_v)
        detalhes_caminho.append({
            "id": id_v,
            "nome": vertice.nome,
            "lat": vertice.lat,
            "lon": vertice.lon
        })

    return jsonify({
        "path": detalhes_caminho,
        "distance": distancia if distancia != float('inf') else None,
        "has_path": distancia != float('inf')
    })

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)