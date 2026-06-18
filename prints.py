def print_pedidos():
    print("""
=========================================================
                         Pedidos
=========================================================
(1) Em produção
(2) Finalizados
(3) Desistências""")

    tipo_servico = input("Qual tipo de serviço você deseja visualizar? ")
    return tipo_servico

def print_service():
    print("""
=========================================================
                    SERVIÇOS
=========================================================""")
    print("""
(1) Reforma
(2) Bainha
(3) Confecção
(4) Ajuste
(5) Conserto""")

    escolha = input("Escolha uma opção: ")
    return int(escolha)

def print_start_menu():
    print("""
=========================================================
                   Projeto Sogrinha
=========================================================
(1) Clientes
(2) Serviços
(3) Pedidos
(4) Sair""")

    user_menu_input = input("Escolha uma opção: ")
    return user_menu_input