import function_clientes
import inicialize_db
import prints
from cmdcommands import limpar_tela, voltar_cor, mudar_cor

loop = True
fim_loop_servico = ""
results = []
#Retorna a conexao e o cursor da inicialize_db
conexao, cursor = inicialize_db.inicialize_tables()

#estilizando o cmd antes de entrar no loop
limpar_tela()
mudar_cor()

while loop:

    user_menu_input = prints.print_start_menu()
    limpar_tela()

    if user_menu_input == "1":
        print("""
(1) Ver informações dos clientes
(2) Cadastrar cliente""")

        cadastro_ou_info = input("Escolha uma opção: ")
        limpar_tela()

        if cadastro_ou_info == "1":
            function_clientes.clients_info(cursor)
        elif cadastro_ou_info == "2":
            function_clientes.cadastrar_clientes(conexao, cursor)

    elif user_menu_input == "2":
        print("""Qual cliente deseja os seus serviços?
(1) Digite o nome do cliente
(2) Digite o CPF do cliente""")

        user_service_menu_input = input("Escolha uma opção: ")
        limpar_tela()

        fim_loop_servico, lista_servicos, cliente_id = function_clientes.checar_cliente_existe_e_passar_pro_loop(cursor, user_service_menu_input)

        if fim_loop_servico == "n":
            limpar_tela()
            print(f"Os serviços escolhidos foram: {(", ".join(lista_servicos))}")
            valor_servico = input("Qual o valor do serviço?")
            confirmando = input("Deseja salvar as alterações? [S/N]").lower()
            limpar_tela()

            if confirmando == "s":

                function_clientes.adiciona_servicos_escolhidos(conexao, cursor, cliente_id, lista_servicos)

                cursor.execute("""UPDATE clientes SET valor = ?, status = ? WHERE id = ?""",
                               (float(valor_servico), "Em produção", cliente_id))
                conexao.commit()

        elif fim_loop_servico == "cadastre":
            print("Esse cliente ainda não foi cadastrado")
            novo_cadastro = input("Deseja cadastrar esse cliente? [S/N]").lower()
            limpar_tela()
            if novo_cadastro == "s":
                function_clientes.cadastrar_clientes(conexao, cursor)

        elif fim_loop_servico == "Comando Inválido":
            print(fim_loop_servico)

    elif user_menu_input == "3":
        limpar_tela()
        tipo_servico = prints.print_pedidos()
        limpar_tela()

        if tipo_servico == "1":
            function_clientes.pega_pedidos_com_status_escolhido(cursor, "Em produção")
        elif tipo_servico == "2":
            function_clientes.pega_pedidos_com_status_escolhido(cursor, "Feito")
        elif tipo_servico == "3":
            function_clientes.pega_pedidos_com_status_escolhido(cursor, "Desistência")

    elif user_menu_input == "4":
        loop = False


voltar_cor()