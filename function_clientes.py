import prints

digitou_errado = "Comando Inválido"

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

def update_pedido_info(conexao, cursor, pedido_id):
    new_status = "Em produção"
    choose_new_status = input("""Qual o novo status do pedido?
(1) Em produção
(2) Feito
(3) Desistência""")

    if choose_new_status == "1":
        new_status = "Em produção"
    elif choose_new_status == "2":
        new_status = "Feito"
    elif choose_new_status == "3":
        new_status = "Desistência"
    else:
        print(digitou_errado)
        return

    cursor.execute("""UPDATE servicos SET status = ? WHERE cliente_id = ?""",
                   (new_status, pedido_id))

    conexao.commit()


def asking_if_wanna_edit(conexao, cursor, where_am_i):
    if where_am_i == "cliente":
        text_question = "Deseja editar os dados do cliente? [S/N] "
    elif where_am_i == "pedido":
        text_question = "Deseja editar o status do pedido? [S/N] "
    else:
        print("Variável where_am_i está incorreta")
        return

    pergunta_editar_cliente = input(text_question).lower()

    if pergunta_editar_cliente == "s":
        edit_id = input(f"Escolha o número do {where_am_i} que deseja editar: ")
        try:
            edit_id = int(edit_id)

            if where_am_i == "cliente":
                update_clients_info(conexao, cursor, edit_id)
            elif where_am_i == "pedido":
                update_pedido_info(conexao, cursor, edit_id)

        except ValueError:
            print("Tem que ser um número")

    elif pergunta_editar_cliente == "n":
        return
    else:
        print(digitou_errado)

def pega_pedidos_com_status_escolhido(cursor, status):
    print(f"""
=========================================================
                      {status.upper()}
=========================================================\n""")
    cursor.execute("""SELECT clientes.id, clientes.nome, GROUP_CONCAT(servicos.descricao, ', '), SUM(servicos.valor)
                      FROM clientes
                      JOIN servicos
                        ON servicos.cliente_id = clientes.id
                      WHERE servicos.status = (?)
                      GROUP BY clientes.id""",
                      (status,))

    pedidos = cursor.fetchall()

    for pedido in pedidos:
        print(f"({pedido[0]}) Name: {pedido[1].capitalize()} / Servicos: {pedido[2]} / Valor: {pedido[3]}")
        print("--------------------------------------------------------------------------")

def loop_escolher_servicos():
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
            print(digitou_errado)
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
        return digitou_errado, "", ""

    results = cursor.fetchone()
    if results:
        fim_loop_servico, dict_servicos_valores = loop_escolher_servicos()
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

