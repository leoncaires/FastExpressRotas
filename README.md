# FastExpressRotas

**Sistema de roteirização dinâmica para entregas utilizando o algoritmo de Dijkstra.**

---

## Integrantes

| Nome | RA |
|------|----|
| Leonel Santos Caires | 41074475 |
| Matheus Henrique da Trindade | 40855783 |
| Elton dos Santos Rodrigues | 38490005 |

---

## 📝 Contribuições dos Integrantes

| Integrante | Principais atividades |
|------------|----------------------|
| **Leonel Santos Caires** | Implementação do algoritmo de Dijkstra com min‑heap, desenvolvimento do servidor Flask e endpoints REST (`app.py`), integração com Socket.IO, simulação de trânsito (`traffic_simulator.py`), extração da malha viária real com OSMnx (`gerar_grafo.py`), recálculo dinâmico, lógica de eficiência, documentação dos documentos E1, E2 e E3, README, testes unitários e de integração. |
| **Matheus Henrique da Trindade** | Melhorias no mapa e interface Leaflet, implementação do sistema de eventos negativos na rota (acidentes e congestionamentos), suporte à visualização das rotas e ajustes de usabilidade no front‑end. |
| **Elton dos Santos Rodrigues** | Desenvolvimento do front‑end com HTML, CSS e JavaScript, exibição das rotas e percurso detalhado, estilização da interface, implementação dos botões de controle (Iniciar/Parar Entrega, Simular Evento), e suporte à correção de exibição de eficiência. |

---

## Contexto e Motivação
A transportadora **FastExpress** precisa realizar entregas com rapidez, mas enfrenta imprevistos como acidentes e congestionamentos.  
Sistemas de navegação comuns oferecem uma rota inicial, porém não se adaptam quando as condições do trânsito mudam após o veículo já estar em movimento.

O **FastExpressRotas** modela a malha viária como um grafo direcionado e ponderado e utiliza o **algoritmo de Dijkstra** para recalcular rotas dinamicamente sempre que um evento de trânsito é detectado.  
O sistema foi projetado para demonstrar, na prática, os conceitos de **caminho mínimo**, **atualização dinâmica de pesos** e **simulação de eventos** em um cenário real de logística urbana.

---

## Objetivo Geral

Desenvolver um WebApp para a FastExpress que, utilizando um grafo direcionado e ponderado, calcule rotas otimizadas e permita atualizar os pesos dinamicamente (devido a acidentes ou congestionamentos), recalculando a rota em tempo real.

---

## Algoritmo e Complexidades

| Algoritmo | Dijkstra com heap de prioridade |
|-----------|----------------------------------|
| Categoria | Guloso |
| Complexidade de tempo | **O((V + E) log V)** |
| Complexidade de espaço | **O(V)** |
| Parada antecipada | Sim (ao atingir o destino) |
| Otimização extra | Lazy deletion (entradas obsoletas na heap são ignoradas) |

---

## Lógica do Sistema

### 1. Modelagem da malha viária como grafo
- **Vértices** = cruzamentos, praças, viadutos (extraídos do OpenStreetMap com OSMnx).
- **Arestas** = vias com geometria real, nome de rua e peso (tempo de percurso em minutos).
- **Peso** = comprimento da via ÷ velocidade média de 30 km/h.
- **Grafo direcionado** que respeita os sentidos reais das ruas (mão única / dupla).
- **Representação interna**: lista de adjacência.

### 2. Cálculo da rota mínima (Dijkstra)
1. Usuário seleciona origem e destino na interface.
2. Front‑end envia `POST /api/rota` com os IDs dos vértices.
3. Servidor executa o algoritmo de Dijkstra com heap de prioridade.
4. Retorna a sequência de vértices do caminho, o tempo total, as ruas percorridas e a geometria da rota.
5. Front‑end desenha a rota verde no mapa e exibe o resumo textual.

### 3. Simulação de eventos de trânsito
- **Simulador automático**: thread que a cada 20s escolhe uma aresta aleatória e aplica:
  - Congestionamento (peso × fator 1.5–3.0).
  - Acidente (peso = ∞, via bloqueada).
- **Simulador manual**: botão “Simular Evento na Rota Atual” que aplica o evento na aresta mais pesada do caminho atual.
  - O evento altera o peso da aresta **no grafo em memória** e emite um sinal via Socket.IO.

### 4. Recálculo dinâmico da rota
1. O evento de trânsito modifica o peso de uma aresta no grafo.
2. O simulador emite um evento `traffic_event` via Socket.IO.
3. O front‑end recebe o evento e chama novamente `POST /api/rota`.
4. O Dijkstra é executado sobre o grafo **com os pesos atualizados**.
5. A nova rota é desenhada no mapa e o painel é atualizado com o novo tempo e a eficiência.

### 5. Relatório de eficiência
- O tempo da primeira rota calculada (antes de eventos) é armazenado.
- A cada recálculo, a eficiência é exibida como:  
`((tempo_inicial − tempo_atual) / tempo_inicial) × 100%`
- Um valor **negativo** indica que o evento piorou o trânsito, mas o algoritmo encontrou a melhor alternativa possível.

---

## Arquitetura do Sistema

O projeto segue uma arquitetura em **4 camadas** (mais uma camada de testes):

| Camada | Responsabilidade | Principais artefatos |
|--------|------------------|----------------------|
| **Apresentação** | Interface web com mapa interativo (Leaflet). Exibe rotas e interage com o usuário. | `app.py` (Flask), `templates/index.html`, `static/script.js`, `static/map.js`, `static/style.css` |
| **Aplicação** | Orquestração: recebe requisições, chama Dijkstra, gerencia simulação e eventos. | `service/route_service.py`, `service/traffic_simulator.py`, `service/event_handler.py` |
| **Domínio** | Modelo do grafo (vértice, aresta) e implementação pura do algoritmo de Dijkstra. | `core/graph.py`, `core/vertex.py`, `core/edge.py`, `algorithms/dijkstra.py` |
| **Infraestrutura** | Leitura/escrita de dados e geração de grafos a partir do OpenStreetMap. | `io/file_reader.py`, `io/gerar_grafo.py`, `io/report_writer.py` |
| **Testes** | Testes unitários e de integração para todos os módulos principais. | `tests/test_dijkstra.py`, `tests/test_graph.py`, `tests/test_events.py`, `tests/test_integration.py` |

**Comunicação em tempo real:** Flask‑SocketIO com `gevent` — a thread do simulador envia eventos ao front‑end via WebSocket sem bloquear o servidor.

## Métricas do Sistema

| Métrica | Valor |
|---------|-------|
| Algoritmo principal | Dijkstra com heap de prioridade |
| Complexidade de tempo | O((V + E) log V) |
| Complexidade de espaço | O(V) |
| Tamanho típico do grafo | ~200 vértices, ~500 arestas |
| Tempo de execução por consulta | < 50 ms |
| Frequência do simulador automático | A cada 20 segundos |
| Latência de atualização | Instantânea via WebSocket |
| Cobertura geográfica | Raio de 1200 m da Praça da Sé, São Paulo |
| Precisão da rota | Geometria real das vias (coordenadas do OpenStreetMap) |
| Eficiência (relatório) | Cálculo percentual em tempo real na interface |

## Ferramentas e Bibliotecas

| Ferramenta/Biblioteca | Uso no projeto |
|-----------------------|----------------|
| **Python 3.10+** | Linguagem principal |
| **Flask** | Servidor web e API REST |
| **Flask-SocketIO** | Comunicação em tempo real (WebSocket) |
| **gevent** | Servidor assíncrono para Flask-SocketIO |
| **Leaflet.js** | Mapa interativo no front‑end |
| **OpenStreetMap (OSM)** | Base de dados geográficos e tiles do mapa |
| **OSMnx** | Extração e modelagem da malha viária real |
| **Shapely** | Manipulação de geometrias (LineString) |
| **Requests** | Chamadas à API externa OSRM |
| **scikit-learn** | Cálculo de vizinhos mais próximos no OSMnx |
| **unittest** | Framework de testes unitários |
| **Socket.IO (client)** | Atualização dinâmica da interface |
| **HTML5 / CSS3 / JavaScript** | Construção da interface web |
| **Git / GitHub** | Controle de versão e repositório remoto |

## Como Executar o Projeto

### Pré‑requisitos
- Python 3.10+
- Pip
- Conexão com internet (na primeira execução, para baixar o mapa)

### Instalação
```bash
git clone https://github.com/leoncaires/FastExpressRotas.git
cd FastExpressRotas
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

```

### Execução

```bash
# Comando para rodar o MVP
# Antes de iniciar o projeto gere o grafo com 
python src/io/gerar_grafo.py
# Depois inicie o servidor
python src/web/app.py

Acesse: http://127.0.0.1:5000

#Resultado da execução
Carregando grafo do OpenStreetMap...
 Grafo gerado com sucesso!
   Vértices: 245
   Arestas:  612
Iniciando simulador e servidor...
 * Running on http://127.0.0.1:5000

```
### Execução de Testes
```bash
#Executar os testes
# Windows PowerShell (na raiz do projeto):
$env:PYTHONPATH="."
python -m unittest discover -s tests -p "test_*.py" -v
# A saída deve mostrar 9 testes com status ok.
```