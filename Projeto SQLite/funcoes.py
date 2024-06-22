import sqlite3

def conectar_db():
        """
        Conecta no banco de dados utilizado e retona a conexão e o cursor para evitar ter que copiar o path da bd muitas vezes
        """
        conn = sqlite3.connect('C:\\Users\\dougl\\OneDrive\\Área de Trabalho\\Douglas\\Programacao\\Python\\Projeto SQLite\\Estoque.db')
        cursor = conn.cursor()
        
        return conn, cursor


def close_conn(conn):
        """"Fecha a conexão com o bd para evitar a repetição dos comandos"""
        conn.commit()
        conn.close()


def adicionar_produto(self) -> str:
        """Recebe um produto em forma de objeto e adiciona seus atributos ao bd"""
        conn, cursor = conectar_db()

        cursor.execute("""
                INSERT INTO produtos (nome, descricao, quantidade_estoque, preco)
                VALUES (?, ?, ?, ?);""", (self.nome, self.descricao, self.quantidade_estoque, self.preco))
        conn.commit()
        conn.close()

        return f"Produto adicionado com sucesso!"

def criar_venda(self) -> None:
        
        conn, cursor = conectar_db()

        cursor.execute("""
                INSERT INTO vendas (id_produto, quantidade_vendida, data_venda)
                VALUES (?, ?, ?);""", (self.id_produto, self.quantidade_vendida, self.data))
        
        cursor.execute(f"""
                UPDATE produtos
                SET quantidade_estoque = (quantidade_estoque - {self.quantidade_vendida})
                WHERE id_produto = {self.id_produto}
        """)

        close_conn(conn)


def consulta_relatorio_geral() -> list:
        conn, cursor = conectar_db()

        cursor.execute("""
                SELECT produtos.nome, produtos.quantidade_estoque, produtos.preco, SUM(vendas.quantidade_vendida) AS Numero_vendas, SUM(vendas.quantidade_vendida * produtos.preco) AS Valor_Total
                FROM produtos LEFT JOIN vendas 
                ON produtos.id_produto = vendas.id_produto
                GROUP BY produtos.id_produto
        """)
        rows = cursor.fetchall()
        close_conn(conn)

        #with open('C:\\Users\\dougl\\OneDrive\\Área de Trabalho\\Douglas\\Programação\\Python\\Projeto SQLite\\relatorio.txt', 'a') as file:
        #        file.write(f"\n     RELATORIO GERAL DE VENDAS:\n")
        #        file.write("=" * 100)
        #        file.write("\n      Produto      |  Quantidade no estoque  |  Preço  |  Numero de vendas  |  Lucro Total   \n")
        #        file.write(f'-' * 100)
        #        
        #        for row in rows:
        #              nome, quantidade_estoque, preco, vendas, valor_total = row
        #              file.write(f"\n{nome:^18} | {quantidade_estoque:^20} | {preco:^10} | {vendas:^16} | {round(valor_total, 2):^13} \n")  
        #        
        #        file.write('-' * 100)                          
        return rows

def consulta_ver_produtos(id_produto):
        conn, cursor = conectar_db()

        cursor.execute(f"""
                SELECT nome, descricao, quantidade_estoque, preco
                FROM produtos 
                WHERE id_produto = {id_produto}
        """)
        
        row = cursor.fetchall()
        close_conn(conn)
        return row