import os
from Classes import Produtos, Cliente

def cadastro_produto(produto):
    produtos_dict = {}
    if os.path.exists('produtos.txt'):
        with open('produtos.txt', 'r') as arquivo:
            for linha in arquivo:
                nome, preco, qtd_estoque, min_estoque = linha.strip().split(';')
                produtos_dict[nome] = Produtos(nome, float(preco), int(qtd_estoque), int(min_estoque))
    if produto.nome in produtos_dict:
        produtos_dict[produto.nome].add_estoque(produto.qtd_estoque)
    else:
        produtos_dict[produto.nome] = produto
    with open('produtos.txt', 'w') as arquivo:
        for p in produtos_dict.values():
            arquivo.write(f'{p.nome};{p.preco};{p.qtd_estoque};{p.min_estoque}\n')
    return list(produtos_dict.values())

def cadastro_vendas(venda):
    vendas = []
    if not os.path.exists('vendas.txt'):
        with open('vendas.txt', 'w') as arquivo:
            arquivo.write(f'{venda.produto};{venda.qtd};{venda.forma_pagamento};{venda.data};{venda.cliente}\n')
    else:
        with open('vendas.txt', 'a') as arquivo:
            arquivo.write(f'{venda.produto};{venda.qtd};{venda.forma_pagamento};{venda.data};{venda.cliente}\n')
    produtos_dict = {}
    with open('produtos.txt', 'r') as arquivo:
        for linha in arquivo:
            nome, preco, qtd_estoque, min_estoque = linha.strip().split(';')
            produtos_dict[nome] = Produtos(nome, float(preco), int(qtd_estoque), int(min_estoque))
    prod_obj = produtos_dict[venda.produto]
    prod_obj.remover(venda.qtd)
    vendas.append(venda)
    with open('produtos_temp.txt', 'w') as f:
        for p in produtos_dict.values():
            f.write(f'{p.nome};{p.preco};{p.qtd_estoque};{p.min_estoque}\n')
    os.remove('produtos.txt')
    os.rename('produtos_temp.txt', 'produtos.txt')
    return vendas, list(produtos_dict.values())

def adicionar_produto(nome_produto, qtd):
    produtos_dict = {}
    with open('produtos.txt', 'r') as arquivo:
        for linha in arquivo:
            nome, preco, qtd_estoque, min_estoque = linha.strip().split(';')
            prod_obj = Produtos(nome, float(preco), int(qtd_estoque), int(min_estoque))
            produtos_dict[nome] = prod_obj
    if nome_produto in produtos_dict:
        prod_obj = produtos_dict[nome_produto]
        prod_obj.add_estoque(int(qtd))

    else:
        raise ValueError(f'Produto {nome_produto} não encontrado.')
    with open('produtos_temp.txt', 'w') as arquivo:
        for p in produtos_dict.values():
            arquivo.write(f'{p.nome};{p.preco};{p.qtd_estoque};{p.min_estoque}\n')
    os.remove('produtos.txt')
    os.rename('produtos_temp.txt', 'produtos.txt')
    return list(produtos_dict.values())

def mostrar_produtos (produtos):
    print('Produtos cadastrados:\n')
    for i in produtos:
        print(i.resumo())
        if i.precisa_repor():
            print(f'O produto {i.nome} precisa ser reposto!')
        
def mostrar_vendas (vendas):
    print('Vendas cadastradas:\n')
    for i in vendas:
        print(i.resumo())
        print(f'Imposto estimado (5%): R${i.calcular_imposto():.2f}')

def listar_clientes():
    clientes = []
    if os.path.exists('clientes.txt'):
        with open('clientes.txt', 'r') as arquivo:
            for linha in arquivo:
                cpf, nome, data_nasc, telefone, endereco = linha.strip().split(';')
                cliente = Cliente(cpf, nome, data_nasc, '', telefone)
                cliente.endereco = endereco
                clientes.append(cliente)
    return clientes


def cadastro_cliente(cliente):
    clientes_dict = {c.cpf: c for c in listar_clientes()}  
    clientes_dict[cliente.cpf] = cliente 

    with open('clientes.txt', 'w') as arquivo:
        for i in clientes_dict.values():
            arquivo.write(f'{i.cpf};{i.nome};{i.data_nasc};{i.telefone};{i.endereco}\n')
    return list(clientes_dict.values())


def mostrar_clientes():
    return listar_clientes()
