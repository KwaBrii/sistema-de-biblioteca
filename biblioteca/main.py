# Melhoria para o futuro: Adicionar ID de livros, adicionar quantidades do mesmo livro disponíveis

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
    autor_normalizado = autor.strip().lower()
    titulo_normalizado = titulo.strip().lower()

# Checa se o livro + autor é repetido, pois livros podem ter o mesmo nome
    for livro in livros:
        if  (
            livro["titulo"].strip().lower() == titulo_normalizado
            and
            livro["autor"].strip().lower() == autor_normalizado
        ):
            print("\nEsse livro já está cadastrado.")
            return

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

# Limita o texto para não quebrar a tabela de exibição
def limitar_texto(texto, tamanho):
    if len(texto) > tamanho:
        return texto[:tamanho - 4] + "..."
    return texto

def listar_livros(livros):
    if not livros:
        print("\nNenhum livro cadastrado.")
        return
# <25 reserva 25 caracteres para o texto a linha à esquerda
    print("\n=== LIVROS CADASTRADOS ===")
    print(f"{'Nº':<4}{'Título':<30}{'Autor':<20}{'Status'}")
    print("-" * 75)

    for indice, livro in enumerate(livros, start=1):
        titulo = limitar_texto(livro["titulo"], 30)
        autor = limitar_texto(livro["autor"], 20)
        
        print(
            f"{indice:<4}"
            f"{titulo:<30}"
            f"{autor:<20}"
            f"{livro['status']}"
        )

# Função de emprestar o livro, impede empréstimo duplicado checando se o livro já foi emprestado, atualiza os dados no JSON, checa se o livro existe no JSON
def emprestar_livro(livros):
    titulo = input(
        "Digite o título do livro: "
    ).strip()

    titulo_normalizado = titulo.lower()
    for livro in livros:
        if livro["titulo"].strip().lower() == titulo_normalizado:
            if livro["status"] == "emprestado":
                print(
                    f"\nO livro já está emprestado para "
                    f"{livro['usuario']}."
                )
                return

            usuario = input(
                "Nome de quem está retirando: "
            ).strip()

            livro["status"] = "emprestado"
            livro["usuario"] = usuario

            salvar_livros(livros)
            print("\nLivro emprestado com sucesso!")
            return
    print("\nLivro não encontrado.")

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