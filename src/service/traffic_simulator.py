import random
import time
import threading

class SimuladorTransito:
    """Simula a obtenção de dados de trânsito em tempo real."""

    def __init__(self, grafo, funcao_retorno):
        self.grafo = grafo
        self.funcao_retorno = funcao_retorno
        self.thread = None
        self.executando = False

    def _executar_simulacao(self):
        while self.executando:
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
                # Se a aresta já está bloqueada, mantém o bloqueio e apenas notifica
                if aresta_escolhida.peso == float('inf'):
                    mensagem = (
                        f"Tentativa de congestionamento na via {id_origem}->{aresta_escolhida.destino}, "
                        f"mas a via já está bloqueada por acidente."
                    )
                else:
                    aresta_escolhida.peso = int(aresta_escolhida.peso * fator)
                    mensagem = (
                        f"Congestionamento na via {id_origem}->{aresta_escolhida.destino}. "
                        f"Peso multiplicado por {fator} (Novo tempo: {aresta_escolhida.peso} min)."
                    )
            elif tipo_evento == "acidente":
                aresta_escolhida.peso = float('inf')
                mensagem = (
                    f"ACIDENTE GRAVE na via {id_origem}->{aresta_escolhida.destino}. "
                    f"Via bloqueada!"
                )

            self.funcao_retorno(mensagem)
            time.sleep(20)

    def aplicar_evento_manual(self, id_origem, id_destino, tipo="congestionamento", fator=3.0):
        """
        Aplica um evento em uma aresta específica e retorna a mensagem.
        Chamado via API para simular evento na rota atual.
        """
        arestas = self.grafo.obter_adjacentes(id_origem)
        for aresta in arestas:
            if aresta.destino == id_destino:
                if tipo == "acidente":
                    aresta.peso = float('inf')
                    mensagem = f"Acidente simulado em {id_origem}→{id_destino}. Via bloqueada!"
                else:
                    # Se a aresta já está bloqueada, mantém o bloqueio
                    if aresta.peso == float('inf'):
                        mensagem = (
                            f"Tentativa de congestionamento em {id_origem}→{id_destino}, "
                            f"mas a via já está bloqueada por acidente."
                        )
                    else:
                        aresta.peso = int(aresta.peso * fator)
                        mensagem = f"Congestionamento simulado em {id_origem}→{id_destino}. Peso multiplicado por {fator}."
                # Notifica os clientes via callback
                self.funcao_retorno(mensagem)
                return mensagem
        return f"Aresta {id_origem}→{id_destino} não encontrada."

    def iniciar(self):
        if not self.executando:
            self.executando = True
            self.thread = threading.Thread(target=self._executar_simulacao)
            self.thread.daemon = True
            self.thread.start()

    def parar(self):
        self.executando = False