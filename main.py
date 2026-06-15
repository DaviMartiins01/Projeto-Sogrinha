import sqlite3
import function_clientes

lista_de_servicos = ["Reforma", "Bainha", "Confecção", "Ajuste", "Conserto"]
continuar = ""

conexao = sqlite3.connect("clientes.db")
cursor = conexao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
                                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                                            nome TEXT NOT NULL, 
                                            CPF TEXT NOT NULL UNIQUE,
                                            numero TEXT,
                                            status TEXT,
                                            valor INTEGER
                                                                )""")

cursor.execute ("""CREATE TABLE IF NOT EXISTS servicos (
                   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   cliente_id INTEGER NOT NULL,
                   descricao TEXT NOT NULL
                   )""")

conexao.commit()

print("""
(1) Cadastrar Clientes
(2) Serviços
(3) Pedidos""")

user_menu_input = input("Escolha uma opção: ")

if user_menu_input == "1":
    nome_cliente = input("Informe o nome do cliente: ")
    cpf_cliente = input("Informe o CPF do cliente: ")
    numero_cliente = input("Informe o numero do cliente: ")

    cursor.execute("""INSERT INTO clientes (nome, cpf, numero) VALUES (?, ?, ?)""",
                   (nome_cliente, cpf_cliente, numero_cliente))
    conexao.commit()
    print("Cliente cadastrado com sucesso!")

elif user_menu_input == "2":
    print("""Qual cliente deseja os seus serviços?
(1) Digite o nome do cliente
(2) Digite o CPF do cliente""")

    user_service_menu_input = input("Escolha uma opção: ")

    if user_service_menu_input == "1":
        checar_nome_cliente = input("Informe o nome do cliente: ")
        cursor.execute("""SELECT * FROM clientes WHERE nome = ?""",
                       (checar_nome_cliente,))
        if cursor.fetchone():
            escolha = function_clientes.print_service()
            print(lista_de_servicos[escolha - 1])
        else:
            print("Esse cliente ainda não foi cadastrado")

    if user_service_menu_input == "2":
        checar_CPF_cliente = input("Informe o CPF do cliente: ")
        cursor.execute("SELECT * FROM clientes WHERE cpf = ?",
                       (checar_CPF_cliente,))

        if cursor.fetchone():
            while continuar != "n":
               escolhendo_servico = function_clientes.print_service()

               cursor.execute("SELECT id FROM clientes WHERE cpf = ?",
                              (checar_CPF_cliente,))
               cliente_id = cursor.fetchone()[0]

               cursor.execute("""INSERT INTO servicos (cliente_id, descricao) VALUES (?, ?)""",
                              (cliente_id,lista_de_servicos[escolhendo_servico - 1]))
               conexao.commit()
               continuar = input("Deseja continuar escolhendo serviços? [S/N]").lower()

        else:
            print("Esse cliente ainda não foi cadastrado")


elif user_menu_input == "3":
    print("Pedidos")
