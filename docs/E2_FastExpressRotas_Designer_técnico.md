# E2 — Design Técnico, Arquitetura e Backlog

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 21 de abril de 2026  
> **Peso:** 20% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | FastExpressRota |
| Repositório GitHub | https://github.com/leoncaires/FastExpressRotas |
| Integrante 1 | Leonel Santos Caires — RA: 41074475 |
| Integrante 2 | Matheus Henrique da Trindade — RA: 40855783 |
| Integrante 3 | Elton dos Santos Rodrigues — RA: 38490005 |

---

## 1. Algoritmos Escolhidos

### 1.1 Algoritmo Principal

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Dijkstra |
| Categoria | Guloso |
| Complexidade de tempo | O((V+E) log V) |
| Complexidade de espaço | O(V) |
| Problema que resolve | Caminho mínimo de uma única origem para todos os demais vértices em um grafo com pesos não negativos |

**Por que este algoritmo foi escolhido?**

O problema do FastExpressRota consiste em encontrar a rota de menor tempo de viagem em uma malha viária, onde os pesos das arestas são sempre positivos (tempos em minutos). Dijkstra é o algoritmo clássico para este cenário, pois garante a solução ótima em grafos com pesos não negativos. O algoritmo pode ser implementado com uma condição de parada ao atingir o vértice de destino, tornando-o adequado para consultas de origem-destino como as do sistema. Além disso, sua complexidade O((V+E) log V) é eficiente para malhas viárias (grafos esparsos), e sua estrutura gulosa permite recálculos rápidos após eventos simulados (acidente/congestionamento)

**Alternativa descartada e motivo:**

| Algoritmo alternativo | Motivo da exclusão |
|----------------------|-------------------|
| Bellman-Ford | Embora aceite pesos negativos, sua complexidade O(V*E) é muito pior que a de Dijkstra, tornando-o inviável para grafos de grande porte. Conforme o artigo do Medium (Patrão, s.d.), Dijkstra é superior em desempenho quando todos os pesos são não negativos, que é o caso do problema. |
| A* (A-Estrela) | O A* é um algoritmo de busca informada que pode ser mais rápido em termos práticos, mas exige uma heurística admissível (como distância de Manhattan). Em mapas de grade com custos uniformes, o A* tem desempenho promissor. No entanto, no cenário do FastExpressRota, os pesos representam tempos de viagem que não são perfeitamente proporcionais à distância geográfica (devido a limites de velocidade, semáforos, etc.), tornando difícil garantir uma heurística admissível e consistente. Portanto, Dijkstra é a escolha mais segura para garantir otimalidade. |

**Limitações no contexto do problema:**

- O Dijkstra não lida com atualizações dinâmicas de pesos. Após um evento (congestionamento), é necessário executar o algoritmo novamente a partir do vértice atual, o que é computacionalmente viável para o porte esperado do grafo.
- Não funciona com pesos negativos, mas isso não se aplica ao domínio de tempos de viagem.

**Referência bibliográfica:**

RIOS, Marcel L.; S. NETO, Francisco S.; NETTO, José F. Magalhães. Análise e Comparação dos Algoritmos de Dijkstra e A-Estrela na Descoberta de Caminhos Mínimos em Mapas de Grade. In: ENCONTRO DE TEORIA DA COMPUTAÇÃO (ETC), 1., 2016, Porto Alegre. Anais [...]. Porto Alegre: Sociedade Brasileira de Computação, 2016. p. 887-890. DOI: https://doi.org/10.5753/etc.2016.9852. Disponível em: https://sol.sbc.org.br/index.php/etc/article/view/9852. Acesso em: 19 abr. 2026.

---

### 1.2 Algoritmo Adicional *(se houver)*

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Nenhum (apenas Dijkstra é suficiente para os requisitos) |
| Categoria |  |
| Complexidade de tempo |  |
| Complexidade de espaço |  |

**Justificativa:**
O escopo do projeto limita-se ao cálculo de rotas mínimas com recálculo após eventos pontuais. O algoritmo de Dijkstra, com condição de parada ao atingir o destino, atende plenamente todos os requisitos funcionais. A implementação de um segundo algoritmo não traria benefícios adicionais dentro do prazo e complexidade definidos. Embora o A* possa ser mais eficiente em cenários com heurísticas bem definidas, a garantia de otimalidade do Dijkstra é mais adequada para um sistema de logística onde precisão é crítica.


**Referência bibliográfica:**
PATRÃO, Brian. Dijkstra's vs Bellman-Ford Algorithm. Medium, [s.d.]. Disponível em: https://medium.com/@brianpatrao1996/dijkstras-vs-bellman-ford-algorithm-383e4771c2cb. Acesso em: 19 abr. 2026.


---

## 2. Arquitetura em Camadas

> Insira o diagrama abaixo. Pode ser exportado do Draw.io, Excalidraw, etc.

![Diagrama de arquitetura](./docs/E2_FastExpressRotas.jpeg)

### Descrição das camadas

| Camada | Responsabilidade | Artefatos principais |
|--------|-----------------|----------------------|
| Apresentação (UI/CLI) | Interface web com mapa interativo. Exibe rotas sobre mapa real. | `src/web/app.py` (Flask), `templates/index.html`, `static/style.css`, `static/script.js`, `static/map.js` |
| Aplicação (Service) | Orquestração: recebe requisições, chama Dijkstra, retorna caminho + coordenadas. | `src/service/route_service.py`, `src/service/event_handler.py` |
| Domínio (Core) | Modelagem do grafo (vértices, arestas) e implementação do algoritmo de Dijkstra. Contém a lógica pura de caminho mínimo. | `src/core/graph.py`, `src/core/vertex.py`, `src/core/edge.py`, `src/algorithms/dijkstra.py` |
| Infraestrutura (I/O) | Leitura do dataset inicial (malha viária com coordenadas), geração de grafos reais e salvamento de relatórios. | `src/io/file_reader.py`, `src/io/report_writer.py`, `src/io/gerar_grafo.py` |

---

## 3. Estrutura de Diretórios

```
fast-express-rota/
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
```

> **Justificativa de desvios** *(se houver)*:

- **`src/io/gerar_grafo.py`**: Adicionado para automatizar a extração da malha viária real do OpenStreetMap, gerando o arquivo `malha_exemplo.json` com coordenadas reais e geometria das vias.
- **`src/service/traffic_simulator.py`**: Implementa a simulação de trânsito (automática e manual) com alteração dinâmica dos pesos, funcionalidade central para demonstrar o recálculo de rotas.
- **`src/service/event_handler.py`**: Mantido como esqueleto para gerenciamento de eventos, complementando o simulador.

Essas adições não alteram a arquitetura de 4 camadas planejada; apenas enriquecem as camadas de Aplicação e Infraestrutura.

---

## 4. Definição do Dataset

**Formato de entrada aceito:**

JSON contendo vértices com coordenadas geográficas (latitude e longitude) e arestas com peso (tempo em minutos), nome e geometria.

**Exemplo de estrutura do arquivo de entrada:**

```json
{
 "vertices": [
    { "id": 0, "nome": "Centro", "lat": -23.5505, "lon": -46.6333 },
    { "id": 1, "nome": "Bairro A", "lat": -23.5612, "lon": -46.6558 },
    { "id": 2, "nome": "Bairro B", "lat": -23.5754, "lon": -46.6221 },
    { "id": 3, "nome": "Industrial", "lat": -23.5401, "lon": -46.6702 }
  ],
  "arestas": [
    { "origem": 0, "destino": 1, "peso": 8, "nome": "Rua Exemplo", "geometry": [[-23.5505, -46.6333], [-23.5510, -46.6340]] },
    { "origem": 1, "destino": 0, "peso": 8, "nome": "Rua Exemplo", "geometry": [[-23.5510, -46.6340], [-23.5505, -46.6333]] }
  ]
}
```

**Estratégia de geração aleatória:**

| Parâmetro | Descrição |
|-----------|-----------|
| Número de vértices | Obtidos das tags name do OSM ou, na ausência, dos nomes das ruas incidentes. |
| Região geográfica | Ponto central (Praça da Sé, São Paulo) com raio de 1500 m, usando dist_type='network' para garantir conectividade. |
| Fonte de dados | OpenStreetMap, extraídos via OSMnx. |
| Peso das arestas | Comprimento da via (metros) ÷ 30 km/h, convertido para minutos. |
| Geometria | Coordenadas reais da via (LineString do Shapely). |
| Arestas reversas | Adicionadas para permitir manobras e desvios. |

---

## 5. Backlog do Projeto

### 5.1 In-Scope — O que será implementado

| # | Funcionalidade | Prioridade | Critério de aceite |
|---|---------------|------------|-------------------|
| 1 | Modelagem do grafo viário. Carregar malha a partir de arquivo JSON. | Alta | Dado um arquivo JSON válido com vértices e arestas, quando o sistema iniciar, então o grafo é carregado em memória e está pronto para consultas. |
| 2 | Cálculo de rota inicial. Executar Dijkstra entre origem e destino informados. | Alta | Dado um grafo carregado e vértices de origem e destino válidos, quando o usuário solicitar a rota, então o sistema retorna a sequência de vértices do caminho mínimo e o tempo total estimado. |
| 3 | Simulação de acidente. Aumentar drasticamente o peso de uma aresta (ou bloqueá-la). | Média | Dada uma rota calculada, quando o usuário selecionar uma aresta e aplicar o evento "acidente", então o peso da aresta se torna infinito (ou muito alto) e a rota é recalculada automaticamente a partir do vértice atual do veículo. |
| 4 | Simulação de congestionamento. Multiplicar o peso de uma aresta por fator configurável. | Média | Dada uma rota calculada, quando o usuário aplicar o evento "congestionamento" com fator 2.0 em uma aresta, então o peso da aresta dobra e o sistema recalcula a rota a partir da posição atual. |
| 5 | Relatório de eficiência. Comparar tempo da rota original (sem eventos) com tempo da rota dinâmica (após recálculos). | Baixa | Dado um cenário de simulação com pelo menos um evento, quando a entrega for concluída, então o sistema exibe a diferença percentual entre o tempo planejado e o tempo real. |
| 6 | Interface Web simplificada. Página com seleção de origem/destino, visualização textual da rota e botões para eventos. | Alta | Dado o servidor Flask em execução, quando o usuário acessar a URL raiz, então uma página HTML permite escolher vértices, calcular rota e acionar eventos, exibindo resultado atualizado. |
| 7 | Visualização da rota em mapa interativo – Exibir grafo e caminho mínimo sobre mapa Leaflet/OpenStreetMap. | Média | Dado um grafo com coordenadas geográficas (lat/lon) e uma rota calculada, quando o usuário solicitar a visualização, então o sistema gera um mapa interativo com a rota destacada e marcadores de origem/destino, utilizando Folium/Leaflet, sem necessidade de chaves de API pagas. |

### 5.2 Out-of-Scope — O que NÃO será feito

| Funcionalidade excluída | Motivo |
|------------------------|--------|
| Roteirização com múltiplos veículos (frota) | O projeto foca em um único veículo realizando uma entrega. |
| Persistência de histórico de rotas em banco de dados | Apenas geração de relatório em memória/arquivo é exigida. |
| Atualização dinâmica de trânsito em tempo real (via API externa) | Os eventos são simulados manual e automaticamente, não integrados com fontes externas. |


---

## Checklist de Entrega

- [X] Big-O de tempo e espaço declarados para cada algoritmo
- [X] Ao menos 1 alternativa descartada com justificativa
- [X] Diagrama de arquitetura com 4 camadas identificadas
- [X] Referência bibliográfica para cada algoritmo (ABNT ou IEEE)
- [X] Backlog com ≥ 5 itens In-Scope e ≥ 3 Out-of-Scope
- [X] Ao menos 3 critérios de aceite no formato "dado / quando / então"
- [X] Exemplo de estrutura de arquivo de entrada presente

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
