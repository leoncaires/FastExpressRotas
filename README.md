# FastExpressRotas

Sistema Web para cálculo dinâmico de rotas com o algoritmo de Dijkstra, aplicado à logística de entregas.

## Como executar o MVP

1. Clone o repositório

2. Crie e ative um ambiente virtual:
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

3. Instale as dependências:
pip install -r requirements.txt

4. Execute a aplicação Flask:
cd src
python app.py

5. Acesse: http://127.0.0.1:5000

## Executando os testes
python -m unittest discover tests/

