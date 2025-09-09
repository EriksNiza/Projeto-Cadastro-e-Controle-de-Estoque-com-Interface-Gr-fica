import os
from Classes import Produtos, Vendas

produto = Produtos('cappuccino', 10.00, 11, 14)

def cadastro (produto):
    produtos = []
    if not os.path.exists('produtos.txt'):
        with open ('produtos.txt','w') as arquivo:
            arquivo.write (f'{produto.nome};{produto.preco};{produto.qtd_estoque};{produto.min_estoque}\n')
    else:
        with open ('produtos.txt','a') as arquivo:
            arquivo.write (f'{produto.nome};{produto.preco};{produto.qtd_estoque};{produto.min_estoque}\n')
    with open ('produtos.txt', 'r') as arquivo:
        for linha in arquivo:
            nome, preco, qtd_estoque, min_estoque = linha.strip().split(';')
            produtos.append(Produtos(nome, float(preco), int(qtd_estoque), int(min_estoque)))
    return produtos


def cadastro_vendas(venda):
    vendas = []
    if not os.path.exists ('vendas.txt', 'w'):
        with open ('vendas.txt', 'w') as arquivo:
            arquivo.write (f'{venda.produto};{venda.qtd};{venda.forma_pagamento};{venda.data}\n')
    else:
        with open ('vendas.txt', 'a') as arquivo:
            arquivo.write (f'{venda.produto};{venda.qtd};{venda.forma_pagamento};{venda.data}\n')
    with open ('vendas.txt','r') as arquivo:
        for linha in arquivo:
            produto, qtd, forma_pagamento, data = linha.strip().split(';')
            vendas.append(Vendas(produto, int(qtd), forma_pagamento, data))
    with open ('produtos.txt','r') as arquivo:
        for linha in arquivo:
            if venda.produto == linha.nome:
                qtd = Produtos.remover(qtd)
                with open ('produtos.txt','w')
                    arquivo.write (f'{}')
            

produtos = cadastro(produto)
for i in produtos:
    print (f'Nome: {i.nome} | Preço: R${i.preco} | Quantidade em estoque: {i.qtd_estoque} | Quantidade minima em estoque: {i.min_estoque}')