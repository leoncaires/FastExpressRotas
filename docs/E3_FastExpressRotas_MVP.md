# E3 — MVP: Núcleo Funcional com Primeiras Telas

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 15 de maio de 2026  
> **Peso:** 25% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | FastExpressRotas |
| Repositório GitHub | https://github.com/leoncaires/FastExpressRotas |
| Integrante 1 | Leonel Santos Caires — 41074475 |
| Integrante 2 | Elton dos Santos Rodrigues — 38490005 |
| Integrante 3 | Matheus Henrique da Trindade — 40855783 |

---

## 1. Como Executar o MVP

> Instrua como rodar o projeto do zero. Alguém que nunca viu o código deve conseguir executar seguindo estas instruções.

**Pré-requisitos:**

```bash
# Python 3.10 ou superior e pip instalados
python --version   # Deve mostrar 3.10+
pip --version
```

**Instalação:**

```bash
# Clone e instale dependências
git clone https://github.com/leoncaires/FastExpressRotas.git
cd FastExpressRotas
# Crie e ative o ambiente virtual
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

**Execução:**

```bash
# Comando para rodar o MVP
# Antes de iniciar o projeto gere o grafo com 
python src/io/gerar_grafo.py
# Depois inicie o servidor
python src/web/app.py

Acesse: http://127.0.0.1:5000

```

**Saída esperada:
```bash 
#Resultado da execução
Carregando grafo do OpenStreetMap...
 Grafo gerado com sucesso!
   Vértices: 245
   Arestas:  612
Iniciando simulador e servidor...
 * Running on http://127.0.0.1:5000
```
**

```
# Cole aqui um exemplo real da saída do seu programa
# Onde irá haver o recálculo dinâmico de 20 em 20 segundos das rotas que temos no nosso projeto dentro do raio de 1200. Alguns exemplos:
Evento de trânsito: Congestionamento na via 60685853->2390933497. Peso multiplicado por 2.8 (Novo tempo: 0 min).
Evento de trânsito: Congestionamento na via 4509498149->4802625028. Peso multiplicado por 2.4 (Novo tempo: 0 min).
Evento de trânsito: ACIDENTE GRAVE na via 457039860->4823032881. Via bloqueada!
```

---

## 2. Algoritmo Implementado

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Dijkstra (caminho mínimo com heap de prioridade) |
| Arquivo de implementação | src/algorithms/dijkstra.py |
| Complexidade de tempo | O((V + E) log V) |
| Complexidade de espaço | O(V) |

**Trecho do código com comentário de Big-O:**

```python
def dijkstra(grafo, id_inicio, id_alvo=None):
    # Verifica se o vértice inicial existe no grafo – O(1)
    if id_inicio not in grafo.vertices:
        return {}, {}

    # Inicializa distâncias e antecessores – O(V)
    distancias = {v: float('inf') for v in grafo.vertices}
    antecessores = {v: None for v in grafo.vertices}
    distancias[id_inicio] = 0

    # Fila de prioridade (min-heap) – O(1)
    fila_prioridade = [(0, id_inicio)]

    # Loop principal – executa até V vezes no pior caso
    while fila_prioridade:
        # Extrai o vértice com menor distância – O(log V)
        dist_atual, id_atual = heapq.heappop(fila_prioridade)

        # Lazy deletion: ignora entradas antigas – O(1)
        if dist_atual > distancias[id_atual]:
            continue

        # Parada antecipada ao atingir o destino – O(1)
        if id_alvo is not None and id_atual == id_alvo:
            break

        # Explora arestas vizinhas – O(grau) por vértice, total O(E)
        for aresta in grafo.obter_adjacentes(id_atual):
            nova_dist = dist_atual + aresta.peso    # O(1)
            if nova_dist < distancias[aresta.destino]:
                distancias[aresta.destino] = nova_dist
                antecessores[aresta.destino] = id_atual
                # Insere na heap – O(log V)
                heapq.heappush(fila_prioridade, (nova_dist, aresta.destino))

    return distancias, antecessores
```

---

## 3. Estrutura do Repositório

> Confirme que a estrutura implementada está de acordo com o E2.

FastExpressRotas/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── docs/
│   ├── E1_FastExpressRotas_Documento De Visão.md
│   ├── E2_FastExpressRotas_Designer_técnico.md   
│   ├── E3_FastExpressRotas_MVP.md    
│   └── imagens/
│       ├── E1_FastExpressRotas.jpeg
│       ├── E2_FastExpressRotas.png
│       ├── E3_mvp_entrada.png
│       └── E3_mvp_resultado.png
│
├── src/
│   ├── core/                         # Camada de Domínio
│   │   ├── graph.py
│   │   ├── vertex.py
│   │   └── edge.py
│   │
│   ├── algorithms/                   # Algoritmos de Grafos
│   │   └── dijkstra.py
│   │
│   ├── io/                           # Camada de Infraestrutura (I/O)
│   │   ├── file_reader.py
│   │   ├── report_writer.py
│   │   └── gerar_grafo.py
│   │
│   ├── service/                      # Camada de Aplicação (Service)
│   │   ├── route_service.py
│   │   ├── event_handler.py
│   │   └── traffic_simulator.py
│   │
│   ├── web/                          # Camada de Apresentação (Flask)
│   │   ├── app.py
│   │   ├── templates/
│   │   │   └── index.html
│   │   └── static/
│   │       ├── cargotruck.png
│   │       ├── style.css
│   │       ├── script.js
│   │       └── map.js                # inicialização e controle do mapa 
│   │
│   └── main.py                       # Ponto de entrada opcional
│
├── tests/
│   ├── test_graph.py
│   ├── test_dijkstra.py
│   ├── test_events.py
│   └── test_integration.py
│
└── data/
    ├── malha_exemplo.json
    └── grafos_aleatorios/            # gerados durante testes        # ou pom.xml, package.json…

**Desvios em relação ao E2** *(se houver)*:
- **`src/io/gerar_grafo.py`**: Script adicional para extrair a malha viária real do OpenStreetMap usando OSMnx. Não estava previsto, mas tornou-se necessário para gerar automaticamente o arquivo `malha_exemplo.json` com nomes de ruas e geometria das vias.
- **`src/service/traffic_simulator.py`**: Implementa a simulação de eventos de trânsito (congestionamentos e acidentes) que alteram os pesos do grafo em tempo real. Substitui a ideia inicial de um `event_handler.py` genérico, oferecendo uma thread automática e um método para eventos manuais.
- **`src/service/event_handler.py`**: Mantido como esqueleto de gerenciador de eventos, mas a funcionalidade real foi concentrada no simulador.

---

## 4. Telas do MVP

> Insira screenshots ou gravações da interface funcionando.

### Tela de Entrada

![Tela de entrada](./docs/imagens/E3_mvp_entrada.png)

*Descrição: Tela inicial padrão da funcionalidade do algoritmo onde exibe o mapa centralizado de São Paulo com um raio de 1200m onde A transportadora irá agir com ês botões principais: Calcular Rota (Real) (OSRM), Calcular Rota Interna (Dijkstra) e Simular Evento na Rota Atual. Uma barra amarela no topo notifica eventos de trânsito simulados em tempo real. *

### Tela de Resultado

![Tela de resultado](./docs/imagens/E3_mvp_resultado.png)

*Descrição: Após clicar em “Calcular Rota Interna (Dijkstra)”, a rota verde é desenhada no mapa e o painel à esquerda exibe: 
Origem e destinos resumidos, percurso detalhado expansível (ao clicar em “Ver percurso detalhado”), tempo total em minutos (com duas casas decimais), eficiência: comparação percentual com o tempo inicial da rota e ao clicar em “Simular Evento”, um congestionamento (ou acidente) é aplicado na aresta mais pesada da rota, e a rota é recalculada automaticamente, atualizando o texto e o traçado verde.*

---

## 5. Testes Unitários

| Algoritmo | Caso de teste | Status | Comando para executar |
|-----------|--------------|--------|----------------------|
| Dijkstra | Caso base | ✅  | `python -m unittest tests.test_dijkstra.TesteDijkstra.testar_caso_base` |
| Dijkstra | Grafo vazio | ✅ | `python -m unittest tests.test_dijkstra.TesteDijkstra.testar_grafo_vazio` |
| Dijkstra | Grafo completo | ✅ | `python -m unittest tests.test_dijkstra.TesteDijkstra.testar_grafo_completo`|
| Grafo (Graph) | Adicionar vértice | ✅ | `python -m unittest tests.test_graph.TesteGrafo.testar_adicionar_vertice`|
| Grafo (Graph) | Adicionar aresta e verificar adjacência | ✅ | `python -m unittest tests.test_graph.TesteGrafo.testar_adicionar_aresta`|
| Eventos | Bloqueio de aresta | ✅ | `python -m unittest tests.test_events.TesteEventos.testar_bloqueio_aresta`|
| Integração | Página inicial retorna 200 | ✅ | `python -m unittest tests.test_integration.TesteIntegracao.testar_pagina_inicial`|
| Integração | API de rota retorna caminho entre vértices reais | ✅ | `python -m unittest tests.test_integration.TesteIntegracao.testar_pagina_inicial`|

**Como rodar todos os testes:**

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

**Resultado atual:**

```
# Cole aqui a saída do pytest / JUnit
testar_caso_base (test_dijkstra.TesteDijkstra.testar_caso_base)
Caso base: caminho mais curto de 0 a 3 é 0->1->2->3 com custo 6. ... ok
testar_grafo_completo (test_dijkstra.TesteDijkstra.testar_grafo_completo)
Caso grafo completo: todos os vértices conectados entre si com peso 1. ... ok
testar_grafo_vazio (test_dijkstra.TesteDijkstra.testar_grafo_vazio)
Caso grafo vazio: Dijkstra deve retornar distâncias vazias. ... ok
testar_bloqueio_aresta (test_events.TesteEventos.testar_bloqueio_aresta)
Caso aplicar acidente bloqueia a aresta. ... ok
testar_adicionar_aresta (test_graph.TesteGrafo.testar_adicionar_aresta)
Caso base: adicionar aresta e verificar adjacência. ... ok
testar_adicionar_vertice (test_graph.TesteGrafo.testar_adicionar_vertice)
Caso base: adicionar vértice deve aumentar contagem. ... ok
testar_adjacencia_vazia (test_graph.TesteGrafo.testar_adjacencia_vazia)
Caso grafo sem arestas: adjacência de vértice sem vizinhos é lista vazia. ... ok
testar_api_rota (test_integration.TesteIntegracao.testar_api_rota)
A API de rota deve retornar caminho para vértices existentes no grafo. ... ok
testar_pagina_inicial (test_integration.TesteIntegracao.testar_pagina_inicial)
A página principal deve retornar status 200. ... ok
```

---

## 6. Histórico de Commits

> Liste os 5+ commits mais relevantes desta entrega.

| Hash (7 chars) | Mensagem | Autor |
|----------------|----------|-------|
| `179fdc4` | feat: Implementando as estruturas iniciais com integração com mapas reais | Matheus |
| `cb80568` | feat: Infraestrutura de dados, com grafo real com os nomes das ruas | Leonel |
| `ae751a3` | test: Simulação de trânsito manual com o endpoint de eventos | Leonel |
| `dd9e745` | feat: Na parte do front com um pouco de estilização, no quesito de exibição das ruas, eficiências e correções | Elton |
| `63abf8c` | fix: Alguns ajustes na questão da simulação | Leonel |
| `3e83e96` | fix: Corrige recálculo dinâmico do Disjkstra | Leonel |
| `61ea867` | feat:Ajustes na aplicação dos src/tests | Matheus |
| `d285906` | docs:Implementação do E3, Imagens do E3 e por fim o Read.me para o E3 MVP | Leonel |
| `6c523be` | fix:Melhoria no mapa e interface | Matheus |
| `6c523be` | feat:Implementação sistema de eventos negativos na rota | Matheus |


---

## 7. O que está funcionando / O que ainda falta

| Funcionalidade | Status | Observação |
|---------------|--------|------------|
| Classe do grafo | ✅ Completo | Lista de adjacência, vértices com coordenadas |
| Algoritmo principal(Dijkstra) | ✅ Completo | Heap de prioridade, parada antecipada, O((V+E) log V) |
| Leitura de arquivo JSON | ✅ Completo | Suporte a vértices, arestas com geometria e nome |
| Tela de entrada (Seleção de Origem/Destino) | ✅ Completo | Dropdowns ordenados com nomes de ruas |
| Tela de resultado(rota + mapa) | ✅ Completo | Rota verde, resumo textual, eficiência |
| Simulador de trânsito | ✅ Completo | Automático (thread) e manual (botão) |
| Recálculo dinâmico | ✅ Completo | Via Socket.IO, atualiza rota sem recarregar página |
| Testes unitários | ✅ Completo | 9 testes passando em todos os cenários |
| Geração de grafo real | ✅ Completo | Script gerar_grafo.py extrai dados do OpenStreetMap |
| Simulação de entrega de carga | ✅ Completo | Encadeamento origem → destino com evento de entrega |
| Geração de grafo real | ✅ Completo | Layout responsivo e tema visual de transportadora |
| Botões e Legendas | ✅ Completo | Faltando aplicar distância apenas na legenda do dijkstra |

---

## Checklist de Entrega

- [X] Repositório público e acessível
- [X] .gitignore configurado
- [X] README com instruções de execução do MVP
- [X] Algoritmo principal executando sem erros
- [X] Tela de entrada e tela de resultado demonstráveis
- [X] 3 testes unitários por algoritmo (mínimo caso base passando)
- [X] ≥ 5 commits com prefixos semânticos (feat:, fix:, test:, docs:)
- [X] Ao menos 1 arquivo de grafo de exemplo em `data/`

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
