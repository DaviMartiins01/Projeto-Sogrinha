import prints

def clients_info(cursor):
    cursor.execute("""SELECT nome, cpf, numero, valor FROM clientes""")
    info = cursor.fetchall()
    print("----------------------------------------------------------------------")
    for client_data in info:
        nome, cpf, numero, valor = client_data
        print(f"Nome: {nome.capitalize()} / CPF: {cpf} / Numero: {numero} / Valor: {valor}")
        print("----------------------------------------------------------------------")


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

def loop_escolher_servicos(results):
    lista_de_servicos = ["Reforma", "Bainha", "Confecção", "Ajuste", "Conserto"]
    lista_de_servicos_escolhidos = []
    continuar_escolhendo = ""

    while continuar_escolhendo != "n":
        escolhendo_servico = int(prints.print_service())

        lista_de_servicos_escolhidos.append(lista_de_servicos[escolhendo_servico - 1])
        continuar_escolhendo = input("Deseja continuar escolhendo serviços? [S/N]").lower()

    return continuar_escolhendo, lista_de_servicos_escolhidos

def checar_cliente_existe_e_passar_pro_loop(cursor, tipo_busca):
    if tipo_busca == "1":
        checar_nome_cliente = input("Informe o nome do cliente: ").lower()

        cursor.execute("""SELECT *
                          FROM clientes
                          WHERE nome = ?""",
                       (checar_nome_cliente,))
    elif tipo_busca == "2":
        checar_cpf_cliente = input("Informe o CPF do cliente: ")
        cursor.execute("SELECT * FROM clientes WHERE cpf = ?",
                       (checar_cpf_cliente,))
    else:
        return "Comando Inválido", "", ""

    results = cursor.fetchone()
    if results:
        fim_loop_servico, lista_servicos = loop_escolher_servicos(results)
        cliente_id = results[0]
        return fim_loop_servico, lista_servicos, cliente_id
    else:
        return "cadastre", "", ""

def adiciona_servicos_escolhidos(conexao, cursor, id_cliente, lista_de_servicos):
    for servico in lista_de_servicos:
        cursor.execute("""INSERT INTO servicos (cliente_id, descricao)
                              VALUES (?, ?)""",
                        (id_cliente, servico))

    conexao.commit()

