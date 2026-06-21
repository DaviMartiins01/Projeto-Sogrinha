import prints

def get_clients_info():
    nome_cliente = input("Informe o nome do cliente: ").lower()
    cpf_cliente = input("Informe o CPF do cliente: ")
    numero_cliente = input("Informe o numero do cliente: ")

    print("Nome do cliente: ", nome_cliente.capitalize())
    print("CPF do cliente: ", cpf_cliente)
    print("Numero do cliente: ", numero_cliente)

    confirm_registration = input("As informações estão corretas? [S/N]").lower()

    return confirm_registration, nome_cliente, cpf_cliente, numero_cliente

def display_clients_info(cursor):
    cursor.execute("""SELECT id, nome, cpf, numero FROM clientes""")
    info = cursor.fetchall()
    print("----------------------------------------------------------------------")
    for client_data in info:
        id, nome, cpf, numero = client_data
        print(f"({id}) Nome: {nome.capitalize()} / CPF: {cpf} / Numero: {numero}")
        print("----------------------------------------------------------------------")

def cadastrar_clientes(conexao, cursor):

    confirm_registration, nome_cliente, cpf_cliente, numero_cliente = get_clients_info()

    if confirm_registration == "s":
        cursor.execute("""INSERT INTO clientes (nome, cpf, numero)
                          VALUES (?, ?, ?)""",
                       (nome_cliente, cpf_cliente, numero_cliente))

        conexao.commit()
        print("Cliente cadastrado com sucesso!")

    elif confirm_registration == "n":
        print("Cliente não cadastrado")

def update_clients_info(conexao, cursor, cliente_id):
    confirm_registration, nome_cliente, cpf_cliente, numero_cliente = get_clients_info()

    if confirm_registration == "s":
        cursor.execute("""UPDATE clientes SET nome = ?, cpf = ?, numero = ?
                          WHERE id = ?""",
                       (nome_cliente, cpf_cliente, numero_cliente, cliente_id))

        conexao.commit()
        print("Cliente atualizado com sucesso!")

def pega_pedidos_com_status_escolhido(cursor, status):
    print(f"""
=========================================================
                      {status.upper()}
=========================================================\n""")
    cursor.execute("""SELECT clientes.nome, GROUP_CONCAT(servicos.descricao, ', '), SUM(servicos.valor)
                      FROM clientes
                      JOIN servicos
                        ON servicos.cliente_id = clientes.id
                      WHERE servicos.status = (?)
                      GROUP BY clientes.id""",
                      (status,))

    pedidos = cursor.fetchall()

    for pedido in pedidos:
        print(f"Name: {pedido[0].capitalize()} / Servicos: {pedido[1]} / Valor: {pedido[2]}")
        print("--------------------------------------------------------------------------")

def loop_escolher_servicos(results):
    lista_de_servicos = ["Reforma", "Bainha", "Confecção", "Ajuste", "Conserto"]
    lista_de_valores = []
    lista_de_servicos_escolhidos = []
    continuar_escolhendo = "s"

    while continuar_escolhendo != "n":
        if continuar_escolhendo == "s":
            escolhendo_servico = int(prints.print_service())

            lista_de_servicos_escolhidos.append(lista_de_servicos[escolhendo_servico - 1])
            valor_servico = float(input("Qual o valor do serviço?"))
            lista_de_valores.append(valor_servico)
            continuar_escolhendo = input("Deseja continuar escolhendo serviços? [S/N]").lower()
        else:
            print("Comando Inválido")
            continuar_escolhendo = input("Deseja continuar escolhendo serviços? [S/N]").lower()

    dict_servicos_valores = dict(zip(lista_de_servicos_escolhidos, lista_de_valores))

    return continuar_escolhendo, dict_servicos_valores

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
        fim_loop_servico, dict_servicos_valores = loop_escolher_servicos(results)
        cliente_id = results[0]
        return fim_loop_servico, dict_servicos_valores ,cliente_id
    else:
        return "cadastre", "", ""

def adiciona_servicos_escolhidos(conexao, cursor, dict_servicos_valores, id_cliente):

    for servico, valores in dict_servicos_valores.items():
        cursor.execute("""INSERT INTO servicos (cliente_id, descricao, status, valor)
                                  VALUES ( ?, ?, ?, ?)""",
                       (id_cliente, servico, "Em produção", valores))

    conexao.commit()

