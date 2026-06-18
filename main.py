import function_clientes
import inicialize_db
from cmdcommands import limpar_tela
from cmdcommands import mudar_cor

loop = True
fim_loop_servico = ""
results = []
#Retorna a conexao e o cursor da inicialize_db
conexao, cursor = inicialize_db.inicialize_tables()

#estilizando o cmd antes de entrar no loop
limpar_tela()
mudar_cor()

while loop:

    user_menu_input = function_clientes.print_start_menu()
    limpar_tela()

    if user_menu_input == "1":
        nome_cliente = input("Informe o nome do cliente: ").lower()
        cpf_cliente = input("Informe o CPF do cliente: ")
        numero_cliente = input("Informe o numero do cliente: ")

        print("Nome do cliente: ", nome_cliente.capitalize())
        print("CPF do cliente: ", cpf_cliente)
        print("Numero do cliente: ", numero_cliente)

        confirm_registration = input("As informações estão corretas? [S/N]").lower()

        if confirm_registration == "s":
            cursor.execute("""INSERT INTO clientes (nome, cpf, numero) VALUES (?, ?, ?)""",
                           (nome_cliente, cpf_cliente, numero_cliente))

            conexao.commit()
            print("Cliente cadastrado com sucesso!")
        elif confirm_registration == "n":
            print("Cliente não cadastrado")


    elif user_menu_input == "2":
        print("""Qual cliente deseja os seus serviços?
(1) Digite o nome do cliente
(2) Digite o CPF do cliente""")

        user_service_menu_input = input("Escolha uma opção: ")
        limpar_tela()

        if user_service_menu_input == "1":
            checar_nome_cliente = input("Informe o nome do cliente: ").lower()

            cursor.execute("""SELECT * FROM clientes WHERE nome = ?""",
                           (checar_nome_cliente,))

            results = cursor.fetchone()

            fim_loop_servico = function_clientes.loop_escolher_servicos(conexao, cursor, results, checar_nome_cliente)
            limpar_tela()

        if user_service_menu_input == "2":
            checar_CPF_cliente = input("Informe o CPF do cliente: ")
            cursor.execute("SELECT * FROM clientes WHERE cpf = ?",
                           (checar_CPF_cliente,))

            results = cursor.fetchone()

            fim_loop_servico = function_clientes.loop_escolher_servicos(conexao, cursor, results, checar_CPF_cliente)
            limpar_tela()

        if fim_loop_servico == "n":
            limpar_tela()
            valor_servico = input("Qual o valor do serviço?")
            cursor.execute("""UPDATE clientes SET valor = ?, status = ? WHERE id = ?""", (float(valor_servico), "Em produção",results[0]))
            conexao.commit()

    elif user_menu_input == "3":
        limpar_tela()
        tipo_servico = function_clientes.print_pedidos()
        limpar_tela()

        if tipo_servico == "1":
            function_clientes.print_pedidos_com_status(cursor, "Em produção")
        elif tipo_servico == "2":
            function_clientes.print_pedidos_com_status(cursor, "Feito")
        elif tipo_servico == "3":
            function_clientes.print_pedidos_com_status(cursor, "Desistência")

    elif user_menu_input == "4":
        loop = False
