import os
from Classes import Produtos, Cliente

def cadastro_produto(produto):
    produtos_dict = {}
    if os.path.exists("produtos.txt"):
        with open("produtos.txt", "r") as arq:
            for linha in arq:
                p = linha.strip().split(";")
                if len(p) == 4:
                    nome, preco, qtd, minimo = p
                    produtos_dict[nome] = Produtos(nome, float(preco), int(qtd), int(minimo))
    if produto.nome in produtos_dict:
        produtos_dict[produto.nome].add_estoque(produto.qtd_estoque)
    else:
        produtos_dict[produto.nome] = produto
    with open("produtos.txt", "w") as arq:
        for p in produtos_dict.values():
            arq.write(f"{p.nome};{p.preco};{p.qtd_estoque};{p.min_estoque}\n")
    return list(produtos_dict.values())

def cadastro_vendas(venda):
    vendas = []
    with open("vendas.txt", "a") as arq:
        arq.write(f"{venda.produto};{venda.qtd};{venda.forma_pagamento};{venda.data};{venda.cliente}\n")
    produtos_dict = {}
    with open("produtos.txt", "r") as arq:
        for linha in arq:
            p = linha.strip().split(";")
            if len(p) == 4:
                nome, preco, qtd, minimo = p
                produtos_dict[nome] = Produtos(nome, float(preco), int(qtd), int(minimo))
    produtos_dict[venda.produto].remover(venda.qtd)
    vendas.append(venda)
    with open("produtos_temp.txt", "w") as f:
        for p in produtos_dict.values():
            f.write(f"{p.nome};{p.preco};{p.qtd_estoque};{p.min_estoque}\n")
    os.remove("produtos.txt")
    os.rename("produtos_temp.txt", "produtos.txt")
    return vendas, list(produtos_dict.values())

def adicionar_produto(nome_produto, qtd):
    produtos_dict = {}
    with open("produtos.txt", "r") as arq:
        for linha in arq:
            p = linha.strip().split(";")
            if len(p) == 4:
                nome, preco, qtd_est, minimo = p
                produtos_dict[nome] = Produtos(nome, float(preco), int(qtd_est), int(minimo))
    if nome_produto in produtos_dict:
        produtos_dict[nome_produto].add_estoque(int(qtd))
    else:
        raise ValueError("Produto não encontrado")
    with open("produtos_temp.txt", "w") as arq:
        for p in produtos_dict.values():
            arq.write(f"{p.nome};{p.preco};{p.qtd_estoque};{p.min_estoque}\n")
    os.remove("produtos.txt")
    os.rename("produtos_temp.txt", "produtos.txt")
    return list(produtos_dict.values())

def mostrar_produtos(produtos):
    for p in produtos:
        print(p.resumo())
        if p.precisa_repor():
            print(f"{p.nome} precisa ser reposto")

def mostrar_vendas(vendas):
    for v in vendas:
        print(v.resumo())
        print(f"Imposto: R${v.calcular_imposto():.2f}")

def listar_clientes():
    clientes = []
    if os.path.exists("clientes.txt"):
        with open("clientes.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split(";")
                if len(partes) == 5:
                    cpf, nome, nasc, tel, end = partes
                    c = Cliente(cpf, nome, nasc, "", tel)
                    c.endereco = end
                    clientes.append(c)
    return clientes

def cadastro_cliente(cliente):
    d = {c.cpf: c for c in listar_clientes()}
    d[cliente.cpf] = cliente
    with open("clientes.txt", "w", encoding="utf-8") as arq:
        for c in d.values():
            arq.write(f"{c.cpf};{c.nome};{c.data_nasc};{c.telefone};{c.endereco}\n")
    return list(d.values())

def mostrar_clientes():
    return listar_clientes()
