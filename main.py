import sqlite3

conexao = sqlite3.connect("clientes.db")
cursor = conexao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
                                            id INTERGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                                            nome TEXT NOT NULL, 
                                            CPF TEXT NOT NULL UNIQUE)""")

conexao.commit()

print("""
(1) Cadastrar Clientes
(2) Serviços
(3) Pedidos""")

user_input = input("Escolha uma opção: ")

if user_input == "1":
    nome_cliente = input("Informe o nome do cliente: ")
    cpf_cliente = input("Informe o CPF do cliente: ")
    numero_cliente = input("Informe o numero do cliente: ")
    print("Cliente cadastrado com sucesso!")

elif user_input == "2":
    checar_nome_cliente = input("Informe o nome do cliente: ")
#     print("""
# =========================================================
#                       SERVIÇOS
# =========================================================""")
#     print("""
# (1) Reforma
# (2) Bainha
# (3) Sob Medida
# (5) Ajuste""")

elif user_input == "3":
    print("Pedidos")
