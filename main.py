import streamlit as st
import os
from arquivos import cadastro_produto, cadastro_vendas
from Classes import Produtos, Vendas

ARQUIVO_PRODUTOS = 'produtos.txt'

with st.sidebar:
    st.title('Menu')
    pagina = st.selectbox(
        'Selecione uma das páginas',
        ['Sobre nós', 'Cadastro de produtos', 'Registro de vendas']
    )

if pagina == 'Sobre nós':
    st.header('Sobre nós')
    st.text('Esta página apresenta o desenvolvimento de um pequeno sistema de controle de estoque voltado para uma cafeteria, simulando uma situação real de mercado. A proposta do projeto é criar uma ferramenta simples e funcional, que possa ser utilizada por pequenos comércios para gerenciar produtos e registrar vendas de forma prática e acessível.')
    st.markdown('---')
    st.text('Feito por: Erik Niza, Heitor Butrico, Henrique Augusto e Leonardo Bredariol - 2ºD DS')

elif pagina == 'Cadastro de produtos':
    st.header('Cadastro de Produtos')

    with st.expander('Registre seus produtos'):
        nome_prod = st.text_input('Insira no nome do produto: ')
        preco_prod = st.number_input('Insira o preço do produto: ', min_value=0.0, step=0.5)
        estoque_prod = st.slider('Insira a quantidade em estoque: ', 0, 200)
        quantMin_prod = st.slider('Quantidade mínima para manter estoque: ', 0, 20)
        enviar_prod = st.button('Enviar')

        if enviar_prod:
            if nome_prod and preco_prod and estoque_prod:
                novo_produto = Produtos(nome_prod, preco_prod, estoque_prod, quantMin_prod)
                produtos = cadastro_produto(novo_produto)
                st.success(f"Produto '{nome_prod}' cadastrado com sucesso!")
            else:
                st.warning('Preencha todos os campos antes de enviar')

    with st.expander('Visualize seus produtos'):
        st.markdown('---')
        if os.path.exists(ARQUIVO_PRODUTOS):
            with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
                produtos = []
                for linha in f:
                    nome, preco, qtd, min_qtd = linha.strip().split(";")
                    produtos.append(Produtos(nome, float(preco), int(qtd), int(min_qtd)))

            if produtos:
                for p in produtos:
                    st.write(p.resumo())
                    if p.precisa_repor():
                        st.warning(f"O produto {p.nome} precisa ser reposto!")
            else:
                st.write("Nenhum registro ainda.")
        else:
            st.write("Nenhum produto cadastrado ainda.")

elif pagina == 'Registro de vendas':
    st.header("Registro de Vendas")

    with st.expander('Registre suas vendas'):
        if os.path.exists(ARQUIVO_PRODUTOS):
            with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
                produtos = []
                for linha in f:
                    nome, preco, qtd, min_qtd = linha.strip().split(";")
                    produtos.append(Produtos(nome, float(preco), int(qtd), int(min_qtd)))

            if produtos:
                nomes_produtos = [p.nome for p in produtos]
                escolha = st.selectbox("Selecione o produto", nomes_produtos)
                qtd_venda = st.number_input("Quantidade", min_value=1, step=1)
                forma_pagamento = st.selectbox("Forma de pagamento", ["Dinheiro", "Cartão", "Pix"])
                enviar_venda = st.button("Registrar Venda")

                if enviar_venda and escolha:
                    produto_escolhido = [p for p in produtos if p.nome == escolha][0]
                    nova_venda = Vendas(produto_escolhido, qtd_venda, forma_pagamento)
                    vendas, produtos_atualizados = cadastro_vendas(nova_venda)
                    st.success("Venda registrada com sucesso!")

    with st.expander("Histórico de Vendas"):
        if os.path.exists("vendas.txt"):
            with open("vendas.txt", "r", encoding="utf-8") as f:
                linhas = f.readlines()
            for linha in linhas:
                produto, qtd, forma_pag, data = linha.strip().split(";")
                st.write(f"{data} | Produto: {produto} | Qtd: {qtd} | Pagamento: {forma_pag}")
        else:
            st.write("Nenhuma venda registrada ainda.")

