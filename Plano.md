## 📐 Pseudocódigo do Sistema

```text
INÍCIO DO SISTEMA

CRIAR lista_de_livros vazia

ENQUANTO sistema estiver ativo:

    MOSTRAR MENU:
        1 - Cadastrar livro
        2 - Listar livros
        3 - Emprestar livro
        4 - Devolver livro
        5 - Buscar livro
        6 - Sair

    LER opção

    SE opção == 1:
        PEDIR título
        PEDIR autor

        CRIAR livro:
            título
            autor
            status = "disponível"
            usuário = vazio

        ADICIONAR livro na lista_de_livros


    SENÃO SE opção == 2:
        PARA cada livro em lista_de_livros:
            MOSTRAR título, autor, status


    SENÃO SE opção == 3:
        PEDIR título do livro

        PROCURAR livro na lista

        SE livro encontrado:
            SE status == "disponível":
                PEDIR nome do usuário
                status = "emprestado"
                usuário = nome
                MOSTRAR "Livro emprestado com sucesso"
            SENÃO:
                MOSTRAR "Livro já emprestado"
        SENÃO:
            MOSTRAR "Livro não encontrado"


    SENÃO SE opção == 4:
        PEDIR título do livro

        PROCURAR livro na lista

        SE livro encontrado:
            SE status == "emprestado":
                status = "disponível"
                usuário = vazio
                MOSTRAR "Livro devolvido"
            SENÃO:
                MOSTRAR "Livro já está disponível"
        SENÃO:
            MOSTRAR "Livro não encontrado"


    SENÃO SE opção == 5:
        PEDIR termo de busca

        PARA cada livro em lista_de_livros:
            SE termo estiver no título OU autor:
                MOSTRAR livro


    SENÃO SE opção == 6:
        ENCERRAR sistema

FIM DO SISTEMA
```
