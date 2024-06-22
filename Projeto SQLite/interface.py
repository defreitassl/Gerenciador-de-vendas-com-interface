import PySimpleGUI as sg
from classes import *
from datetime import datetime

produtos_cadastrados = []
nome_produtos = []
produtos_escolhidos = []
produtos_relatorio = []
database = Database()

sg.theme('DarkBlue')

def janela_editar_produto():
    layout_editar = [
        [sg.Text("Qual campo você quer editar?:")],
        [sg.Combo(values=['Nome', 'Descrição', 'Quantidade em estoque', 'Preço'],key='atributo', size=(20, 1), default_value="Campo")],
        [sg.Text("Digite o novo valor para o campo:")],
        [sg.Input(key='novo_valor', size=(15, 1))],
        [sg.Button('OK', key='ok'), sg.Button('Cancelar', key='cancelar_edicao')]
    ]
    return sg.Window('Editar Produtos', layout_editar, finalize=True, font=('Helvetica', 16), element_justification='center')

tab_cadastro_produtos = [
    [sg.Text("Produto:", size=(8, 1)), sg.Input(key='produto', size=(30, 1))],
    [sg.Text('Descrição:', size=(8, 1)), sg.Multiline(key='descricao', autoscroll=True, size=(40, 2))],
    [sg.Text('Quantidade em estoque:', justification='left'), sg.Text('Preço:', justification='center')],
    [sg.Input(key='quantidade_estoque', size=(18,1)), sg.Input(key='preco', size=(7, 1), justification='center')],
    [sg.Button('Limpar', key='limpar_produtos'), sg.Button("Salvar Produto", key='salvar_produto'), sg.Button("Cancelar", key='cancelar'), sg.Button("Ver produtos", key='ver_produtos')],
    [sg.Combo(nome_produtos, visible=False, default_value='Produtos', key='escolher_produtos', size=(15, 1), s=(15, 1)), sg.Button("Visualizar", key='escolher', visible=False), sg.Button('Deletar', key='deletar_produto', button_color='red', visible=False), sg.Button('Editar', key='editar_produto', visible=False)],
    [sg.Table(produtos_escolhidos, headings=['Nome', 'Descrição', "Quantidade no Estoque", "Preço"], auto_size_columns=True, display_row_numbers=True, key='tabela_produtos', visible=False, size=(300, 3), justification='center'), sg.Button("Limpar", key='limpar_produtos_tabela', visible=False)],
]

tab_cadastro_vendas = [
    [sg.Text("Produto:", size=(12, 1)), sg.Combo(values=[], default_value="Produtos", key='vender_produtos', size=(15, 1), enable_events=True, s=(15, 1))],
    [sg.Text("Quantidade:", size=(12, 1)), sg.Input(key='quantidade', size=(10, 1), enable_events=True), sg.Spin([x for x in range(0, 200)], key='quantidade_spin', enable_events=True)],
    [sg.Text('Data da venda:', size=(12, 1)), sg.Input(key='data', size=(14, 1)), sg.CalendarButton("Escolher data", target='data', format='%y/%m/%d')], 
    [sg.Text("Total:", size=(12, 1)), sg.Text('', key='total')],
    [sg.Button("Gerar venda", key='gerar_venda'), sg.Button("Gerar relatório de vendas", key='relatorio'), sg.Button('Limpar', key='limpar_vendas')]
] 

table_relatorio = [
    [sg.Table(produtos_relatorio, headings = ['Produtos', 'Quantidade estoque', 'Preço', 'Número de vendas', 'Lucro Total'], auto_size_columns=True, display_row_numbers=True, key='tabela_relatorio', justification='center', cols_justification='center')],
    [sg.Button('Fechar', key='fechar_tabela')]
]


layout_tabs = [
    [sg.TabGroup([[sg.Tab("Produtos", tab_cadastro_produtos, element_justification='left', ), sg.Tab('Vendas', tab_cadastro_vendas, element_justification='left'), sg.Tab('Relatório', table_relatorio, visible=False, key='tab_relatorio')]], background_color='black')]
]

layout = [
    [sg.Frame("Gerenciamento de Produtos e Vendas", layout_tabs)],
]

janela, janela_editar = sg.Window("Gerenciamento de produtos", layout, element_justification='center', font=('Helvetica', 16),element_padding=10, size=(1000, 700), finalize=True), None

verprodutos = False

while True:
    window, event, values = sg.read_all_windows()
    
    if window == janela and event in (sg.WIN_CLOSED, 'cancelar'):
        break

    # Código para limpar as informações dos produtos
    elif window == janela and event == 'limpar_produtos':
        janela['produto'].update("")
        janela['descricao'].update("")
        janela['quantidade_estoque'].update("")
        janela['preco'].update("")
    
    # Código para adicionar um produto ao banco de dados
    elif window == janela and event == 'salvar_produto':
        produto = values['produto']
        descricao = values['descricao']
        quantidade_estoque = values['quantidade_estoque']
        preco = values['preco']

        if produto and descricao and quantidade_estoque and preco:
            try:
                quantidade_estoque = int(quantidade_estoque)
                preco = float(preco)
                produto_obj = Produto(produto, descricao, quantidade_estoque, preco)

                produtos_cadastrados.append(produto_obj)

                nome_produtos.append(produto)
                nome_produtos = list(set(nome_produtos))

                janela['escolher_produtos'].update(values=nome_produtos)
                janela['escolher_produtos'].update('Produtos')
                janela['vender_produtos'].update(values=nome_produtos)
                janela['vender_produtos'].update('Produtos')
                produto_obj.adicionar_produto()

                sg.popup_ok("Produto cadastrado com sucesso")

            except ValueError as e:
                sg.popup_error("Quantidade em estoque deve ser um número inteiro e preço deve ser um número válido.")

        else:
            sg.popup_error("Preencha todos os campos para salvar um produto")

    # Código que mostra a parte oculta da tela onde fica a tabela de visualização de produtos e seus botões adicionais
    elif window == janela and event == 'ver_produtos':
        verprodutos = not verprodutos
        janela['escolher_produtos'].update(visible=verprodutos)
        janela['tabela_produtos'].update(visible=verprodutos)
        janela['escolher'].update(visible=verprodutos)
        janela['limpar_produtos_tabela'].update(visible=verprodutos)
        janela['deletar_produto'].update(visible=verprodutos)
        janela['editar_produto'].update(visible=verprodutos)
        janela['ver_produtos'].update("Esconder produtos" if verprodutos else 'Ver produtos')
        janela['escolher_produtos'].update('Produtos')

    # Código para escolher um produto a ser mostrado na tabela
    elif window == janela and event == 'escolher':
        produto = values['escolher_produtos']
        produtos_escolhidos.clear()
        
        for item in produtos_cadastrados:
            
            if item.nome == produto:
                row = consulta_ver_produtos(item.id)
                if row:
                    nome, dsc, qnt, prc = row[0]
                    produtos_escolhidos.append([nome, dsc, qnt, prc])
                break
        
        janela['tabela_produtos'].update(values=produtos_escolhidos)

    # Código para limpar a tabela de vizualização dos produtos
    elif window == janela and event == 'limpar_produtos_tabela':
        produtos_escolhidos.clear()
        janela['tabela_produtos'].update(values=produtos_escolhidos)

    # Código para limpar as informações da parte de vendas
    elif event == 'limpar_vendas':
        janela['quantidade'].update('')
        janela['quantidade_spin'].update(value=0)
        janela['vender_produtos'].update(value='Produtos')
        janela['data'].update('')
        janela['total'].update('')

    elif window == janela and event in ['quantidade', 'quantidade_spin', 'vender_produtos']:
        quantidade = values['quantidade'] if values['quantidade'] else values['quantidade_spin']
        produto_nome = values['vender_produtos']
        
        try:
            quantidade = int(quantidade)
            
            for item in produtos_cadastrados:
               
                if item.nome == produto_nome:
                    total = item.preco * quantidade
                    janela['total'].update(f'R${total:.2f}')
        
        except ValueError:
            janela['total'].update('')
   
    # Código para adicionar um venda ao banco de dados
    elif window == janela and event == 'gerar_venda':
        quantidade = values['quantidade']
        quantidade_spin = values['quantidade_spin']
        produto = values['vender_produtos']
        data = values['data']
        
        if not quantidade:
            quantidade = quantidade_spin

        if quantidade and produto and data:
            try:
                quantidade = int(quantidade)
                data_datetime = datetime.strptime(f"20{data}", "%Y/%m/%d")
                
                for item in produtos_cadastrados:
                    
                    if item.nome == produto:
                        venda_obj = Vendas(item, quantidade, data_datetime)
                        retorno = venda_obj.gerar_venda()              
                        sg.popup_ok(retorno, title="Venda gerada com sucesso")
                        break
            
            except ValueError as e:
                sg.popup_error(f"O atributo de data deve ser no formato 'YY/MM/DD', e o atributo de quantidade deve estar em formato de números")
    
        else:
            sg.popup_error("Complete todos os campos!")
    
    elif window == janela and event == 'relatorio':
        janela['tab_relatorio'].update(visible=True)
        rows = database.gerar_relatorio_geral()

        for row in rows:
            nome, quantidade_estoque, preco, vendas, valor_total = row
            produtos_relatorio.append([nome,quantidade_estoque,preco,vendas,valor_total])
            janela['tabela_relatorio'].update(produtos_relatorio)
    
    elif window == janela and event == 'fechar_tabela':
        janela['tab_relatorio'].update(visible=False)
        produtos_relatorio.clear()
        janela['tabela_relatorio'].update(produtos_relatorio)
    
    elif window == janela and event == 'deletar_produto':
        produto = values['escolher_produtos']

        if produto not in nome_produtos:
                sg.popup_error("Escolha um produto válido no campo de produtos")
        
        else:
            for item in produtos_cadastrados:    
            
                if item.nome == produto:
                    produtos_cadastrados.remove(item)
                    nome_produtos.remove(produto)
                    
                    janela['escolher_produtos'].update(values=nome_produtos)
                    janela['escolher_produtos'].update('Produtos')
                    janela['vender_produtos'].update(values=nome_produtos)
                    janela['vender_produtos'].update('Produtos')
                    
                    retorno = item.deletar_produto()
                    sg.popup(retorno)
                    break
    
    elif window == janela and event == 'editar_produto':
        produto = values['escolher_produtos']

        if produto not in nome_produtos:
            sg.popup_error("Escolha um produto válido no campo de produtos")
        
        else:
            janela_editar = janela_editar_produto()
            janela.hide()
            for item in produtos_cadastrados:
                if item.nome == produto:
                    produto_atual = item
                    break

    elif window == janela_editar:
        if event in (sg.WIN_CLOSED, 'cancelar_edicao'):       
            if janela_editar:
                
                janela_editar.close()
                janela_editar = None
                janela.un_hide()
        
        elif event == 'ok':
            atributo = values['atributo']
            novo_valor = values['novo_valor']

            if atributo == 'Nome':
                atributo = 'nome'
                nome_produtos.remove(produto_atual.nome)
                nome_produtos.append(novo_valor)
                produto_atual.nome = novo_valor
                janela['escolher_produtos'].update('Produtos')
                janela['vender_produtos'].update('Produtos')
                janela['escolher_produtos'].update(values=nome_produtos)
                janela['vender_produtos'].update(values=nome_produtos)
            
            elif atributo == 'Descrição':
                atributo = 'descricao'
                produto_atual.descricao = novo_valor
            
            elif atributo == 'Quantidade em estoque':
                atributo = 'quantidade_estoque'
                produto_atual.quantidade_estoque = int(novo_valor)
            
            elif atributo == 'Preço':
                atributo = 'preco'
                produto_atual.preco = float(novo_valor)
            
            if atributo and novo_valor:
                retorno = produto_atual.editar_produtos(atributo, novo_valor)
                sg.popup(retorno)
                
                if janela_editar:
                    janela_editar.close()
                    janela_editar = None
                    janela.un_hide()

janela.close()