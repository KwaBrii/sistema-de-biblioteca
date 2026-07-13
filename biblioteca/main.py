# Melhoria para o futuro: Adicionar ID de livros, adicionar quantidades do mesmo livro disponíveis
from pathlib import Path
from utils import (normalizar, limitar_texto, confirmar)
from arquivo import (carregar_livros, salvar_livros)
from menu import (mostrar_menu, escolher_ordem, imprimir_cabecalho, imprimir_linha)
import json

# Variáveis de emprestimo para não ocorrer erros de digitação.
STATUS_DISPONIVEL = "disponivel"
STATUS_EMPRESTADO = "emprestado"

# Para encontrar o JSON na pasta certa
ARQUIVO_LIVROS = Path(__file__).parent / "livros.json"

# Centraliza a busca de um livro pelo título
def encontrar_livro(livros, titulo):
    titulo_normalizado = normalizar(titulo)
    for livro in livros:
        if normalizar(livro["titulo"]) == titulo_normalizado:
            return livro
    return None

# Função do cadastro de livros
def cadastrar_livro(livros):
    while True:
        titulo = input("Título do livro: ").strip()
        if titulo:
            break
        print("O título não pode ficar vazio.")
    autor = input("Autor do livro: ").strip()

    # Checa se o livro + autor é repetido, pois livros podem ter o mesmo nome
    for livro in livros:
        if (
            normalizar(livro["titulo"]) == normalizar(titulo)
            and normalizar(livro["autor"]) == normalizar(autor)
        ):
            print("\nEsse livro já está cadastrado.")
            return

    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "status": STATUS_DISPONIVEL,
        "usuario": ""
    }

    # .append vai adicionar o livro ao final da lista no JSON
    livros.append(novo_livro)
    salvar_livros(livros)
    print("\nLivro cadastrado com sucesso!")

# Devolve uma CÓPIA ordenada da lista, sem alterar a ordem original (que é a ordem de cadastro)
def ordenar_livros(livros, criterio):
    if criterio == "titulo":
        return sorted(livros, key=lambda livro: normalizar(livro["titulo"]))
    if criterio == "autor":
        return sorted(livros, key=lambda livro: normalizar(livro["autor"]))
    return livros
 
def listar_livros(livros, criterio="cadastro"):
    if not livros:
        print("\nNenhum livro cadastrado.")
        return
    
    livros_ordenados = ordenar_livros(livros, criterio)
    imprimir_cabecalho("=== LIVROS CADASTRADOS ===")

    for indice, livro in enumerate(livros_ordenados, start=1):
        imprimir_linha(indice, livro)
 
# Usada pelo menu principal, pergunta o critério antes de listar. As outras funções continuam chamando listar_livros() direto, sem esse filtro, para não interromper o fluxo com uma pergunta extra.
def listar_livros_com_filtro(livros):
    criterio = escolher_ordem()
    listar_livros(livros, criterio)

# Função de emprestar o livro, impede empréstimo duplicado checando se o livro já foi emprestado, atualiza os dados no JSON, checa se o livro existe no JSON, lista os livros no inicio da função para quem for alugar se guiar
def emprestar_livro(livros):
    listar_livros(livros)
    titulo = input("\nDigite o título do livro: ").strip()

    livro = encontrar_livro(livros, titulo)
    if not livro:
        print("\nLivro não encontrado.")
        return

    if livro["status"] == STATUS_EMPRESTADO:
        print(f"\nO livro já está emprestado para {livro['usuario']}.")
        return

    usuario = input("Nome de quem está retirando: ").strip()
    livro["status"] = STATUS_EMPRESTADO
    livro["usuario"] = usuario

    salvar_livros(livros)
    print("\nLivro emprestado com sucesso!")

# Segue uma regra bem parecida com a de emprestar, mas troca o status para disponivel e tira o registro de usuário
def devolver_livro(livros):
    titulo = input("\nDigite qual livro deseja devolver: ").strip()

    livro = encontrar_livro(livros, titulo)
    if not livro:
        print("\nLivro não encontrado.")
        return

    if livro["status"] != STATUS_EMPRESTADO:
        print("\nLivro já está disponivel!")
        return

    livro["status"] = STATUS_DISPONIVEL
    livro["usuario"] = ""
    salvar_livros(livros)
    print("\nLivro devolvido com sucesso.")

# Função com termo de busca para livro ou autor
def buscar_livro(livros):
    termo_busca = normalizar(input("\nQual livro ou autor deseja buscar? "))
    criterio = escolher_ordem()
    livros_ordenados = ordenar_livros(livros, criterio)

    imprimir_cabecalho("=== LIVROS ENCONTRADOS ===")
    encontrados = False
    indice = 0

    for livro in livros_ordenados:
        if termo_busca in livro["titulo"].lower() or termo_busca in livro["autor"].lower():
            indice += 1
            imprimir_linha(indice, livro)
            encontrados = True
    if not encontrados:
        print("\nNenhum livro encontrado.")

# Função para deletar um livro da lista
def remover_livro(livros):
    listar_livros(livros)
    titulo = input("\nDigite o título do livro que deseja remover: ").strip()
    livro = encontrar_livro(livros, titulo)
    if not livro:
        print("\nLivro não encontrado.")
        return
        
    if livro["status"] == STATUS_EMPRESTADO:
        print("\nNão é possível remover um livro emprestado.")
        return
    resposta = confirmar(f'\nTem certeza que deseja remover "{livro["titulo"]}"? (S/N): ')

    if resposta == "N":
        print("\nRemoção cancelada.")
        return
    livros.remove(livro)
    salvar_livros(livros)
    print("\nLivro removido com sucesso!")

# Mostra as estatisticas dos livros que temos dados no JSON (total, disponiveis e emprestados) "len()" vai contar quantos elementos existem na lista chamada, e "sum" é literalmente a "soma"
def mostrar_estatisticas(livros):
    total = len(livros)
    disponiveis = sum(1 for livro in livros
        if livro["status"] == STATUS_DISPONIVEL
    )

    emprestados = sum(1 for livro in livros
        if livro["status"] == STATUS_EMPRESTADO
    )

    autores = set()
    for livro in livros:
        autores.add(livro["autor"])

    usuarios = set()
    for livro in livros:
        if livro["status"] == STATUS_EMPRESTADO:
            usuarios.add(livro["usuario"])

    print("\n=== ESTATÍSTICAS ===")
    print(f"Total de livros: {total}")
    print(f"Disponíveis: {disponiveis}")
    print(f"Emprestados: {emprestados}")
    print(f"Autores cadastrados: {len(autores)}")
    print(f"Usuários com empréstimos: {len(usuarios)}")

# Repete uma ação (cadastrar, emprestar, devolver, buscar) enquanto o usuário confirmar com "S" e evita repetir o mesmo bloco "while True + confirmar" quatro vezes dentro do main()
def repetir_acao(funcao, livros, mensagem_confirmacao):
    while True:
        funcao(livros)
        if confirmar(mensagem_confirmacao) == "N":
            break

# Main, one todas as funções agem em conjunto
def main(): 
    livros = carregar_livros()
    acoes = {
        "1": (cadastrar_livro, "\nDeseja cadastrar outro livro? (S/N): "),
        "3": (emprestar_livro, "\nDeseja emprestar outro livro? (S/N): "),
        "4": (devolver_livro, "\nDeseja devolver outro livro? (S/N): "),
        "5": (buscar_livro, "\nDeseja buscar outro livro ou autor? (S/N): "),
        "6": (remover_livro, "\nDeseja remover outro livro? (S/N): "),
    }

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")
        if opcao in acoes:
            funcao, mensagem = acoes[opcao]
            repetir_acao(funcao, livros, mensagem)
        elif opcao == "2":
            listar_livros_com_filtro(livros)
        elif opcao == "7":
            mostrar_estatisticas(livros)
        elif opcao == "8":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()