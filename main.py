print("""
(1) Cadastrar Clientes
(2) Pedidos""")

user_input = input("Escolha uma opção: ")

if user_input == "1":
    nome_cliente = input("Informe o nome do cliente: ")
    cpf_cliente = input("Informe o CPF do cliente: ")
    numero_cliente = input("Informe o numero do cliente: ")
    print("Cliente cadastrado com sucesso!")
    
if user_input == "2":
    print("Pedidos")
