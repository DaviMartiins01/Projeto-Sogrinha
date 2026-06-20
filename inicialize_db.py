import sqlite3

def inicialize_tables():
    conexao = sqlite3.connect("clientes.db")
    cursor = conexao.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
                                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                                            nome TEXT NOT NULL, 
                                            CPF TEXT NOT NULL UNIQUE,
                                            numero TEXT   )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS servicos
                      (
                          id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                          cliente_id INTEGER NOT NULL,
                          descricao TEXT NOT NULL,
                          valor FLOAT,
                          status TEXT  
                                                           
                      )""")


    conexao.commit()

    return conexao, cursor