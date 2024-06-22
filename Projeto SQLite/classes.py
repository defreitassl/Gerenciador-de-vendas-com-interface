from funcoes import *

class Produto:
    id_produto = 1 # Um atributo de classe que atribui um id novo a cada produto criado para assim poder passar o id do produto de forma automática para o objeto de vendas sem ter que pedir o usuário para passar o id toda vez que criar um objeto de venda

    def __init__(self, nome: str, descricao: str, quantidade_estoque: int, preco: float) -> None:
        self.id = Produto.id_produto
        Produto.id_produto += 1
        self.nome = nome
        self.descricao = descricao
        self.quantidade_estoque = quantidade_estoque
        self.preco = round(preco, 2) 
    

    def editar_produtos(self, atributo: any, novo_valor: any) -> str:
        id_produto = self.id
        produto = self
        produto.atributo = novo_valor 

        conn, cursor = conectar_db()
        cursor.execute(f"""
                UPDATE produtos
                SET {atributo} = '{novo_valor}'
                WHERE id_produto = {id_produto}
        """)
        close_conn(conn)

        return"Produto editado com sucesso!"


    def adicionar_produto(self) -> str:
  
        retorno = adicionar_produto(self)
        return retorno


    def deletar_produto(self) -> str:
        id_produto = self.id

        conn, cursor = conectar_db()
        cursor.execute(f"""
                DELETE FROM produtos
                WHERE id_produto = {id_produto}
        """)

        close_conn(conn)
        return "Produto excluído com sucesso!"


class Vendas:
    lista_vendas = []

    def __init__(self, produto: Produto, quantidade_vendida: int, data: any) -> None:
        self.id_produto = produto.id
        self.produto = produto
        self.quantidade_vendida = quantidade_vendida
        self.valor_venda = quantidade_vendida * produto.preco
        self.data = data
        Vendas.lista_vendas += [self]
    

    def gerar_venda(self) -> str:

        criar_venda(self)
        self.produto.quantidade_estoque -= self.quantidade_vendida

        return "Venda gerada!"
    

class Database:

    @staticmethod
    def limpar_tabela():
        conn, cursor = conectar_db()
        cursor.execute(f"""DELETE FROM produtos; 
                          VACUUM;""")
        
        cursor.execute(f"""DELETE FROM vendas; 
                          VACUUM;""")
        close_conn(conn)
        return 'Tabelas limpa com sucesso!'

    @staticmethod
    def gerar_relatorio_geral():
        rows = consulta_relatorio_geral()
        return rows