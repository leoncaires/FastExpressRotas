# FastExpressRotas

**Sistema de roteirização dinâmica para entregas utilizando o algoritmo de Dijkstra.**

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