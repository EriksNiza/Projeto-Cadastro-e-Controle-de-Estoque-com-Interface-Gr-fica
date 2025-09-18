from datetime import datetime
import requests

class Cliente:
    def __init__(self, cpf, nome, data_nasc, cep, telefone):
        self.cpf = str(cpf)
        self.nome = nome.strip().title()
        self.data_nasc = data_nasc
        self.telefone = telefone
        self.endereco = self.buscar_endereco(cep)

    def buscar_endereco(self, cep):
        url = f"https://brasilapi.com.br/api/cep/v1/{cep}"
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            endereco_formatado = (
                f"{dados.get('street', '')}, {dados.get('neighborhood', '')}, "
                f"{dados.get('city', '')} - {dados.get('state', '')}"
            )
            return endereco_formatado
        else:
            return "Endereço não encontrado"

    def resumo(self):
        return (f"CPF: {self.cpf} | Nome: {self.nome} | "
                f"Nascimento: {self.data_nasc} | Telefone: {self.telefone} | "
                f"Endereço: {self.endereco}")

    def salvar_em_arquivo(self, arquivo="clientes.txt"):
        with open(arquivo, "a", encoding="utf-8") as f:
            f.write(f"{self.cpf};{self.nome};{self.data_nasc};{self.telefone};{self.endereco}\n")

class Produtos:

    def __init__(self,nome,preco,qtd_estoque,min_estoque):
        if float(preco) <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        if int(qtd_estoque) < 0:
            raise ValueError("A quantidade em estoque não pode ser negativa.")
        if int(min_estoque) <=0:
            raise ValueError("A quantidade minima em estoque deve ser maior que zero.")
        self.nome=nome
        self.preco=preco
        self.qtd_estoque=qtd_estoque
        self.min_estoque=min_estoque


    def add_estoque(self,qtd):
        if int(qtd)<=0:
             raise ValueError("O numero não pode ser menor igual a 0")
        self.qtd_estoque += int(qtd)
         
    def remover(self,qtd):
        if int(qtd)<=0:
            raise ValueError("O numero não pode ser menor igual a 0")
        if int(qtd)> int(self.qtd_estoque):
            raise ValueError("O numero estoque é insuficiente")
        self.qtd_estoque -= int(qtd)
        return self.qtd_estoque
    
    def precisa_repor(self):
        return self.qtd_estoque <= self.min_estoque

    def resumo(self):
        return f"{self.nome:<15} | Preço: R${self.preco:>7.2f} | Estoque: {self.qtd_estoque}"
    

class Vendas:
    def __init__(self, produto, qtd,cliente, forma_pagamento=None, data=None, ):
        if int(qtd) <= 0:
            raise ValueError("A quantidade da venda deve ser positiva.")
        if int(qtd) > int(produto.qtd_estoque):
            raise ValueError("Estoque insuficiente.")

        self.data = data or datetime.now().strftime("%d/%m/%Y %H:%M")
        self.produto = produto.nome
        self.qtd = qtd
        self.valorTotal = qtd * produto.preco
        self.forma_pagamento = forma_pagamento or "Dinheiro"
        self.cliente=cliente
    def resumo(self):
            return (f"{self.data} | Produto: {self.produto} | "
                f"Qtd: {self.qtd} | Total: R${self.valorTotal:.2f} | "
                f" Pagamento: {self.forma_pagamento} | Cliente: {self.cliente}")
    
    def aplicar_desconto(self, percentual):
        if percentual <= 0 or percentual >= 100:
            raise ValueError("Percentual de desconto inválido.")
        desconto = self.valorTotal * (percentual / 100)
        self.valorTotal -= desconto

    def calcular_imposto(self, taxa=0.07):
         return self.valorTotal * taxa
