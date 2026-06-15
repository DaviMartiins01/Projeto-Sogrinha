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