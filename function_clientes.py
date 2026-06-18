from asyncio.windows_events import NULL

import prints

def cadastrar_clientes(conexao, cursor):
    nome_cliente = input("Informe o nome do cliente: ").lower()
    cpf_cliente = input("Informe o CPF do cliente: ")
    numero_cliente = input("Informe o numero do cliente: ")

    print("Nome do cliente: ", nome_cliente.capitalize())
    print("CPF do cliente: ", cpf_cliente)
    print("Numero do cliente: ", numero_cliente)

    confirm_registration = input("As informações estão corretas? [S/N]").lower()

    if confirm_registration == "s":
        cursor.execute("""INSERT INTO clientes (nome, cpf, numero)
                          VALUES (?, ?, ?)""",
                       (nome_cliente, cpf_cliente, numero_cliente))

        conexao.commit()
        print("Cliente cadastrado com sucesso!")
    elif confirm_registration == "n":
        print("Cliente não cadastrado")


def pega_pedidos_com_status_escolhido(cursor, status):
    print(f"""
=========================================================
                      {status.upper()}
=========================================================\n""")
    cursor.execute("""SELECT clientes.nome, GROUP_CONCAT(servicos.descricao, ', '), clientes.valor
                      FROM clientes
                               LEFT JOIN servicos
                                         ON clientes.id = servicos.cliente_id
                      WHERE clientes.status = (?)
                      GROUP BY clientes.id""",
                      (status,))

    pedidos = cursor.fetchall()

    for pedido in pedidos:
        print(f"Name: {pedido[0].capitalize()} / Servicos: {pedido[1]} / Valor: {pedido[2]}")
        print("--------------------------------------------------------------------------")

def escolher_serviços(conexao, cursor, checar_info, results):
    lista_de_servicos = ["Reforma", "Bainha", "Confecção", "Ajuste", "Conserto"]

    escolhendo_servico = int(prints.print_service())

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
    print(f"Results: {results}")
    if results:
        while continuar_escolhendo != "n":
            escolher_serviços(conexao, cursor, checar_info, results)
            continuar_escolhendo = input("Deseja continuar escolhendo serviços? [S/N]").lower()
    elif not results:
        return "cadastre"

    return continuar_escolhendo