# Melhoria para o futuro: Adicionar ID de livros, adicionar quantidades do mesmo livro disponíveis
from pathlib import Path
import json

# Variáveis de emprestimo para não ocorrer erros de digitação.
STATUS_DISPONIVEL = "disponivel"
STATUS_EMPRESTADO = "emprestado"

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
        json.dump(livros, f, indent=4, ensure_ascii=False)

# Centraliza a normalização de texto (usada em cadastro, busca, empréstimo e devolução)
def normalizar(texto):
    return texto.strip().lower()

# Limita o texto para não quebrar a tabela de exibição
def limitar_texto(texto, tamanho):
    if len(texto) > tamanho:
        return texto[:tamanho - 4] + "..."
    return texto

# Centraliza a busca de um livro pelo título
def encontrar_livro(livros, titulo):
    titulo_normalizado = normalizar(titulo)
    for livro in livros:
        if normalizar(livro["titulo"]) == titulo_normalizado:
            return livro
    return None

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
 
 
# Pergunta ao usuário qual critério de ordenação usar na listagem
def escolher_ordem():
    print("\nComo deseja ordenar a lista?")
    print("1 - Ordem de cadastro (padrão)")
    print("2 - Ordem alfabética (título)")
    print("3 - Autor")
    opcao = input("Escolha uma opção: ").strip()
    return {"1": "cadastro", "2": "titulo", "3": "autor"}.get(opcao, "cadastro")
 
 
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

# Uma função para loop na lista caso a pessoa decida realizar o mesmo tipo de ação várias vezes
def confirmar(mensagem):
    while True:
        resposta = input(mensagem).strip().upper()
        if resposta in ("S", "N"):
            return resposta
        print("Digite apenas S ou N.")

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