# Modularização de arquivos, primeira tentativa

# Centraliza a normalização de texto (usada em cadastro, busca, empréstimo e devolução)
def normalizar(texto):
    return texto.strip().lower()

# Limita o texto para não quebrar a tabela de exibição
def limitar_texto(texto, tamanho):
    if len(texto) > tamanho:
        return texto[:tamanho - 4] + "..."
    return texto

# Uma função para loop na lista caso a pessoa decida realizar o mesmo tipo de ação várias vezes
def confirmar(mensagem):
    while True:
        resposta = input(mensagem).strip().upper()
        if resposta in ("S", "N"):
            return resposta
        print("Digite apenas S ou N.")