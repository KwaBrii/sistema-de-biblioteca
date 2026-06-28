from pathlib import Path
import json

# Para encontrar o JSON na pasta certa
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
        json.dump(
            livros,
            f,
            indent=4,
            ensure_ascii=False
        )

# .strip remove os espaços extras
def cadastrar_livro(livros):
    while True:
        titulo = input("Título do livro: ").strip()
        if titulo:
            break
        print("O título não pode ficar vazio.")

    autor = input("Autor do livro: ").strip()

    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "status": "disponivel",
        "usuario": ""
    }

# .append vai adicionar o livro ao final da lista no JSON
    livros.append(novo_livro)
    salvar_livros(livros)
    print("\nLivro cadastrado com sucesso!")

def listar_livros(livros):
    pass

def emprestar_livro(livros):
    pass

def devolver_livro(livros):
    pass

def buscar_livro(livros):
    pass

# Ainda não sei se te um jeito melhor de fazer isso, talvez uma lista?
def mostrar_menu():
    print("\n===SISTEMA DE BIBLIOTECA===")
    print("1 - Cadastrar livro")
    print("2 - Listar livros")
    print("3 - Emprestar livro")
    print("4 - Devolver livro")
    print("5 - Buscar livro")
    print("6 - Sair")

def main():

    livros = carregar_livros()
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            while True:
                cadastrar_livro(livros)
                continuar = input(
                    "\nDeseja cadastrar outro livro? (S/N): "
                ).strip().upper()

                if continuar == "N":
                    break
                elif continuar != "S":
                    print("Digite apenas S ou N.")
        
        elif opcao == "2":
            listar_livros(livros)

        elif opcao == "3":
            emprestar_livro(livros)

        elif opcao == "4":
            devolver_livro(livros)
        
        elif opcao == "5":
            buscar_livro(livros)

        elif opcao == "6":
            print("Encerrando sistema...")
            break
        
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()