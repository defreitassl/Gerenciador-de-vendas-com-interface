from classes import *

database = Database()
produto_1 = Produto("Biscoito", "Biscoito de maizena Aimoré", 45, 6.30)
produto_2 = Produto("Arroz", "Arroz Branco Integral", 80, 22.10)
produto_3 = Produto("Macarrão", "Macarrão Penne, Dona Lucia", 20, 3.50)
produto_4 = Produto("Panetone", "Pantone trufado meio amargo", 15, 12.90)
produto_5 = Produto("Pão de forma", "Pão de forma integral 0 sal e açúcar", 30, 6.90)


print(produto_1.adicionar_produto())
print(produto_2.adicionar_produto())
print(produto_3.adicionar_produto())
print(produto_4.adicionar_produto())
print(produto_5.adicionar_produto())
