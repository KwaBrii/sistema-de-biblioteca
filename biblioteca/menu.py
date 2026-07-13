from utils import limitar_texto

# Função para mostrar o menu, antes era inteiro na main
def mostrar_menu():
    print("\n===SISTEMA DE BIBLIOTECA===")
    print("1 - Cadastrar livro")
    print("2 - Listar livros")
    print("3 - Emprestar livro")
    print("4 - Devolver livro")
    print("5 - Buscar livro")
    print("6 - Remover Livro")
    print("7 - Estatísticas")
    print("8 - Sair")
 
# Pergunta ao usuário qual critério de ordenação usar na listagem
def escolher_ordem():
    print("\nComo deseja ordenar a lista?")
    print("1 - Ordem de cadastro (padrão)")
    print("2 - Ordem alfabética (título)")
    print("3 - Autor")
    opcao = input("Escolha uma opção: ").strip()
    return {"1": "cadastro", "2": "titulo", "3": "autor"}.get(opcao, "cadastro")

# Cabeçalho da tabela, usado tanto em listar quanto em buscar
def imprimir_cabecalho(titulo_tabela):
    print(f"\n{titulo_tabela}")
    print(f"{'Nº':<4}{'Título':<30}{'Autor':<20}{'Status'}")
    print("-" * 75)

# Imprime uma linha da tabela (um livro), usado em listar e buscar
def imprimir_linha(indice, livro):
    titulo = limitar_texto(livro["titulo"], 30)
    autor = limitar_texto(livro["autor"], 20)
    print(f"{indice:<4}{titulo:<30}{autor:<20}{livro['status']}")