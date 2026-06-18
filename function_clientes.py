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
(1) Cadastrar Clientes
(2) Serviços
(3) Pedidos
(4) Sair""")

    user_menu_input = input("Escolha uma opção: ")
    return user_menu_input

def print_pedidos_em_producao(cursor):
    print("""
=========================================================
                      EM PRODUÇÃO 
=========================================================\n""")
    cursor.execute("""SELECT clientes.nome, GROUP_CONCAT(servicos.descricao, ', '), clientes.valor
                      FROM clientes
                               LEFT JOIN servicos
                                         ON clientes.id = servicos.cliente_id
                      WHERE clientes.status = 'Em produção'
                      GROUP BY clientes.id""")

    pedidos = cursor.fetchall()

    for pedido in pedidos:
        print(f"Name: {pedido[0].capitalize()} / Servicos: {pedido[1]} / Valor: {pedido[2]}")
        print("--------------------------------------------------------------------------")

def escolher_serviços(conexao, cursor, checar_info, results):
    lista_de_servicos = ["Reforma", "Bainha", "Confecção", "Ajuste", "Conserto"]

    escolhendo_servico = int(print_service())

    cursor.execute("SELECT id FROM clientes WHERE cpf = ?",
                    (checar_info,))

    cliente_id = results[0]

    #Adiciona os serviços escolhidos na tabela
    cursor.execute("""INSERT INTO servicos (cliente_id, descricao)
                          VALUES (?, ?)""",
                    (cliente_id, lista_de_servicos[escolhendo_servico - 1]))

    conexao.commit()

def loop_escolher_servicos(conexao, cursor, results, checar_info):
    continuar_escolhendo = ""
    if results:
        while continuar_escolhendo != "n":
            escolher_serviços(conexao, cursor, checar_info, results)
            continuar_escolhendo = input("Deseja continuar escolhendo serviços? [S/N]").lower()
    elif not results:
        print("Esse cliente ainda não foi cadastrado")

    return continuar_escolhendo