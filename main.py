import function_clientes
import inicialize_db
import prints
from cmdcommands import limpar_tela, voltar_cor, mudar_cor

loop = True
fim_loop_servico = ""
results = []
digitou_errado = "Comando Inválido"


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
            function_clientes.display_clients_info(cursor)
            function_clientes.asking_if_wanna_edit(conexao, cursor, "cliente")

        elif cadastro_ou_info == "2":
            function_clientes.cadastrar_clientes(conexao, cursor)
        else:
            print(digitou_errado)

    elif user_menu_input == "2":
        print("""Qual cliente deseja os seus serviços?
(1) Digite o nome do cliente
(2) Digite o CPF do cliente""")

        user_service_menu_input = input("Escolha uma opção: ")
        limpar_tela()

        if user_service_menu_input == "1" or user_service_menu_input == "2":
            fim_loop_servico, dict_servicos_valores ,cliente_id = (function_clientes.checar_cliente_existe_e_passar_pro_loop
                (cursor, user_service_menu_input))

            if fim_loop_servico == "n":
                limpar_tela()
                print(f"Os serviços escolhidos foram: {(", ".join(dict_servicos_valores.keys()))}")
                confirmando = input("Deseja salvar as alterações? [S/N]").lower()
                limpar_tela()

                if confirmando == "s":
                    function_clientes.adiciona_servicos_escolhidos(conexao, cursor, dict_servicos_valores, cliente_id)

            elif fim_loop_servico == "cadastre":
                print("Esse cliente ainda não foi cadastrado")
                novo_cadastro = input("Deseja cadastrar esse cliente? [S/N]").lower()
                limpar_tela()
                if novo_cadastro == "s":
                    function_clientes.cadastrar_clientes(conexao, cursor)

            elif fim_loop_servico == digitou_errado:
                print(fim_loop_servico)
        else:
            fim_loop_servico = digitou_errado



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
        else:
            print(digitou_errado)
            continue

        function_clientes.asking_if_wanna_edit(conexao, cursor, "pedido")

    elif user_menu_input == "4":
        loop = False

    else:
        print(digitou_errado)

voltar_cor()