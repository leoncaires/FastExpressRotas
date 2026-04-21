# E1 — Proposta e Definição do Projeto

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 26 de março de 2026  
> **Peso:** 10% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | FastExpressRotas |
| Integrante 1 | Leonel Santos Caires — RA: 41074475 |
| Integrante 2 | Matheus Henrique da Trindade — RA: 40855783 |
| Integrante 3 | Elton dos Santos Rodrigues — RA: 38490005 |
| Domínio de aplicação | Logística / Gestão de Frota |

---

## 1. Contexto e Motivação

A transportadora FastExpress precisa realizar entregas com rapidez e pontualidade, mas enfrenta imprevistos diários como acidentes, congestionamentos e obras, que podem comprometer os prazos. Sistemas de navegação comuns oferecem uma rota inicial, mas não se adaptam quando as condições do trânsito mudam após o veículo já estar em movimento.
Para resolver esse problema, este projeto propõe um WebApp em Python que modela a malha viária como um grafo e utiliza o algoritmo de Dijkstra para recalcular rotas dinamicamente sempre que um evento (acidente, congestionamento) ocorrer. Dessa forma, os motoristas podem desviar de obstáculos e manter a eficiência das entregas.

---

## 2. Objetivo Geral

Desenvolver um WebApp para a FastExpress que, utilizando um grafo direcionado e ponderado, calcule rotas otimizadas e permita atualizar os pesos dinamicamente (devido a acidentes ou congestionamentos), recalculando a rota em tempo real.

---

## 3. Objetivos Específicos

- [ ] Modelar a região atendida pela FastExpress como um grafo direcionado, onde vértices são cruzamentos e arestas são vias, cada uma com um peso (tempo de percurso) em condições normais.
- [ ] Implementar um mecanismo para alterar os pesos dinamicamente: acidente bloqueia a aresta (peso infinito), congestionamento multiplica o peso por um fator.
- [ ] Aplicar o algoritmo de Dijkstra com heap de prioridade para encontrar o caminho de menor tempo a partir dos pesos atuais.
- [ ] Construir uma interface web por flask onde o gestor da FastExpress informa origem e destino, visualiza a rota e pode simular eventos, onde sistema recalcula a rota se um evento ocorrer durante o trajeto.
- [ ] Avaliar a diferença de tempo total entre a rota estática (sem eventos) e a rota dinâmica (com recálculo), gerando um relatório de eficiência.

---

## 4. Público-Alvo / Caso de Uso Principal

Gestores de frota e motoristas da FastExpress. Exemplo de uso: um gestor define uma rota inicial para uma entrega. No meio do trajeto, um acidente bloqueia uma via. O sistema recebe a informação (simulada), recalcula a rota a partir da posição atual do veículo e exibe um novo caminho, evitando o atraso.

---

## 5. Justificativa Técnica — Por que Grafos?

Uma malha viária é naturalmente um grafo: os cruzamentos são vértices, as vias são arestas. Como ruas podem ter mão única ou dupla, usamos um grafo direcionado, para mão dupla, representamos com duas arestas em sentidos opostos. O tempo de percurso é o "peso", que pode variar conforme o trânsito.

O problema de encontrar a rota mais rápida é um clássico problema de caminho mínimo, resolvido eficientemente por Dijkstra. Como podemos atualizar os pesos a qualquer momento (por eventos simulados), o sistema consegue reagir a imprevistos e recalcular a rota em tempo real. Essa modelagem se encaixa perfeitamente na necessidade da FastExpress, utilizando algoritmos fundamentais da Teoria dos Grafos para garantir a eficiência operacional.
---

## 6. Tipo de Grafo


| Característica | Escolha | Justificativa breve |
|----------------|---------|---------------------|
| Dirigido ou não-dirigido | Dirigido | Para representar mão única e mão dupla (duas arestas opostas) |
| Ponderado ou não-ponderado | Ponderado | O peso é o tempo de percurso, variável conforme eventos. |
| Conectado / bipartido / geral | Geral conexo | A região precisa ser conexa para garantir rota entre qualquer origem e destino. |
| Representação interna pretendida | lista de adjacência | Eficiente para grafos esparsos (malhas viárias) e para atualizar pesos rapidamente. |

---

## 7. Diagrama Conceitual

**Legenda:** 
Círculos: Cruzamentos (Vértices).

Setas: Vias de tráfego (Arestas Direcionadas).

Números: Tempo de percurso em minutos (Pesos).

Linha Amarela: Rota inicial cancelada sugerida pelo sistema.

Linha Verde: Rota atual sugerida pelo sistema.

Ícone Alerta (X): Simulação de acidente para recálculo dinâmico. (nota: caminhos com alerta são considerados de peso infinito / muito alto)** 

---

## Checklist de Entrega

Antes de submeter, confirme:

- [x] Texto entre 300 e 600 palavras (seções 1 a 5)
- [x] Todos os campos da tabela de identificação preenchidos
- [x] Tipo de grafo especificado com justificativa
- [x] Diagrama presente e referenciado no texto
- [x] Arquivo nomeado como `E1_NomeGrupo_Grafos.docx` (versão Word) ou PR aberto (versão GitHub)

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
