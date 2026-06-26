import json

# Não esquecer: "r" = read (ler), "w" = write (escrever), "a" = add (adicionar)
# json.load(f) converte o texto em lista/dicionário
def carregar_livros():
    with open("livros.json", "r", encoding="utf-8") as f:
        livros = json.load(f)

# indent=4 é um padrão de formatação que faz um recuo de 4 espaços, para hierarquia de informações
def salvar_livros(livros):
    with open("livros.json", "w", encoding="utf-8") as arquivo:
        json.dump(
            livros,
            arquivo,
            indent=4,
            ensure_ascii=False
        )