def salvar_relatorio(nome_arquivo: str, conteudo: str):
    """Salva uma string de relatório em arquivo de texto."""
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(conteudo)