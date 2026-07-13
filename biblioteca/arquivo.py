from pathlib import Path
import json

ARQUIVO_LIVROS = Path(__file__).parent / "livros.json"

# Não esquecer: "r" = read (ler), "w" = write (escrever), "a" = add (adicionar)
# json.load(f) converte o texto em lista/dicionário
def carregar_livros():
    try:
        with open(ARQUIVO_LIVROS, "r", encoding="utf-8") as f:
            return json.load(f)
        
    # Caso arquivo JSON seja deletado, cria um novo
    except FileNotFoundError:
        with open(ARQUIVO_LIVROS, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    
# indent=4 é um padrão de formatação que faz um recuo de 4 espaços, para hierarquia de informações
def salvar_livros(livros):
    with open(ARQUIVO_LIVROS, "w", encoding="utf-8") as f:
        json.dump(livros, f, indent=4, ensure_ascii=False)