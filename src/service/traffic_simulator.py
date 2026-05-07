import random
import time
import threading
from src.core.edge import Aresta  


class SimuladorTransito:
    """Simula a obtenção de dados de trânsito em tempo real."""

    def __init__(self, grafo, funcao_retorno):
        self.grafo = grafo
        self.funcao_retorno = funcao_retorno
        self.thread = None
        self.executando = False

    def _executar_simulacao(self):
        while self.executando:
            # Obtém vértices que possuem pelo menos uma aresta de saída
            vertices_com_arestas = [
                id_v for id_v, arestas in self.grafo.lista_adj.items() if arestas
            ]
            if not vertices_com_arestas:
                time.sleep(10)
                continue

            id_origem = random.choice(vertices_com_arestas)
            arestas_saindo = self.grafo.obter_adjacentes(id_origem)
            if not arestas_saindo:
                continue

            aresta_escolhida = random.choice(arestas_saindo)
            tipo_evento = random.choice(["congestionamento", "congestionamento", "acidente"])

            if tipo_evento == "congestionamento":
                fator = round(random.uniform(1.5, 3.0), 1)
                aresta_escolhida.peso = int(aresta_escolhida.peso * fator)
                mensagem = (
                    f"Congestionamento na via {id_origem}->{aresta_escolhida.destino}. "
                    f"Peso multiplicado por {fator} (Novo tempo: {aresta_escolhida.peso} min)."
                )
            elif tipo_evento == "acidente":
                aresta_escolhida.peso = 9999
                mensagem = (
                    f"ACIDENTE GRAVE na via {id_origem}->{aresta_escolhida.destino}. "
                    f"Via bloqueada!"
                )

            self.funcao_retorno(mensagem)
            time.sleep(20)  # Intervalo entre simulações

    def iniciar(self):
        if not self.executando:
            self.executando = True
            self.thread = threading.Thread(target=self._executar_simulacao)
            self.thread.daemon = True
            self.thread.start()

    def parar(self):
        self.executando = False