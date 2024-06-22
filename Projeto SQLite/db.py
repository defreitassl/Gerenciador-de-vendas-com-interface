import sqlite3 

conn = sqlite3.connect('C:\\Users\\dougl\\OneDrive\\Área de Trabalho\\Douglas\\Programacao\\Python\\Projeto SQLite\\Estoque.db')
cursor = conn.cursor()

cursor.execute("""DROP TABLE produtos""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos  (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT NOT NULL UNIQUE,
        quantidade_estoque INTEGER,
        preco FLOAT NOT NULL
    );
""")

cursor.execute("""DROP TABLE vendas""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produto INTEGER NOT NULL,
        quantidade_vendida INTEGER NOT NULL,
        data_venda DATETIME NOT NULL,
        FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
    )
""")

conn.commit()
conn.close()
