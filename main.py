import os
import streamlit as st
from arquivos import cadastro_produto, cadastro_vendas, cadastro_cliente, mostrar_clientes
from Classes import Produtos, Vendas, Cliente

ARQUIVO_PRODUTOS = "produtos.txt"

with st.sidebar:
    st.title("Menu")
    pagina = st.selectbox(
        "Selecione uma das páginas",
        ["Sobre nós", "Cadastro do cliente", "Cadastro de produtos", "Registro de vendas"]
    )

if pagina == "Sobre nós":
    st.header("Sobre nós")
    st.text(
        "Sistema de controle de estoque para uma cafeteria.\n"
        "Permite cadastrar clientes, produtos e registrar vendas."
    )
    st.markdown("---")
    st.text("Feito por: Erik Niza, Heitor Butrico, Henrique Augusto e Leonardo Bredariol - 2ºD DS")

elif pagina == "Cadastro do cliente":
    st.header("Cadastro do cliente")
    with st.expander("Registre o cliente aqui"):
        CPF_cli = st.text_input("CPF")
        nome_cli = st.text_input("Nome")
        dataNasc_cli = st.date_input("Data de nascimento")
        CEP_cli = st.text_input("CEP")
        telefone_cli = st.text_input("Telefone")
        enviar_cli = st.button("Enviar")
        if enviar_cli and CPF_cli and nome_cli and CEP_cli:
            novo_cliente = Cliente(CPF_cli, nome_cli, dataNasc_cli, CEP_cli, telefone_cli)
            cadastro_cliente(novo_cliente)
            st.success(f"Cliente {nome_cli} cadastrado com sucesso!")
    with st.expander("Clientes cadastrados"):
        clientes = mostrar_clientes()
        if clientes:
            for c in clientes:
                st.write(c.resumo())
        else:
            st.write("Nenhum cliente cadastrado.")

elif pagina == "Cadastro de produtos":
    st.header("Cadastro de produtos")
    with st.expander("Registrar produto"):
        nome_prod = st.text_input("Nome do produto")
        preco_prod = st.number_input("Preço", min_value=0.0, step=0.5)
        estoque_prod = st.number_input("Quantidade em estoque", min_value=0, step=1)
        min_estoque = st.number_input("Estoque mínimo", min_value=0, step=1)
        enviar_prod = st.button("Salvar produto")
        if enviar_prod and nome_prod and preco_prod > 0 and min_estoque > 0:
            produto = Produtos(nome_prod, preco_prod, estoque_prod, min_estoque)
            cadastro_produto(produto)
            st.success(f"Produto {nome_prod} cadastrado.")
    with st.expander("Produtos cadastrados"):
        if os.path.exists(ARQUIVO_PRODUTOS):
            with open(ARQUIVO_PRODUTOS, "r") as f:
                produtos = []
                for linha in f:
                    nome, preco, qtd, min_qtd = linha.strip().split(";")
                    produtos.append(Produtos(nome, float(preco), int(qtd), int(min_qtd)))
            if produtos:
                for p in produtos:
                    st.write(p.resumo())
                    if p.precisa_repor():
                        st.warning(f"O produto {p.nome} precisa ser reposto.")
            else:
                st.write("Nenhum produto cadastrado.")
        else:
            st.write("Nenhum produto cadastrado.")

elif pagina == "Registro de vendas":
    st.header("Registro de vendas")
    with st.expander("Registrar venda"):
        produtos = []
        clientes = []
        if os.path.exists(ARQUIVO_PRODUTOS):
            with open(ARQUIVO_PRODUTOS, "r") as f:
                for linha in f:
                    nome, preco, qtd, min_qtd = linha.strip().split(";")
                    produtos.append(Produtos(nome, float(preco), int(qtd), int(min_qtd)))
        clientes = mostrar_clientes()
        if produtos and clientes:
            nomes_produtos = [p.nome for p in produtos]
            nomes_clientes = [c.cpf for c in clientes]
            escolha_prod = st.selectbox("Produto", nomes_produtos)
            escolha_cli = st.selectbox("Cliente (CPF)", nomes_clientes)
            qtd_venda = st.number_input("Quantidade", min_value=1, step=1)
            forma_pag = st.selectbox("Forma de pagamento", ["Dinheiro", "Cartão", "Pix"])
            enviar_venda = st.button("Registrar venda")
            if enviar_venda:
                produto_obj = [p for p in produtos if p.nome == escolha_prod][0]
                cliente_obj = [c for c in clientes if c.cpf == escolha_cli][0]
                venda = Vendas(produto_obj, qtd_venda, cliente_obj.nome, forma_pag)
                cadastro_vendas(venda)
                st.success("Venda registrada.")
        else:
            st.warning("Cadastre ao menos um produto e um cliente.")
    with st.expander("Histórico de vendas"):
        if os.path.exists("vendas.txt"):
            with open("vendas.txt", "r") as f:
                for linha in f:
                    produto, qtd, forma, data, cliente = linha.strip().split(";")
                    st.write(f"{data} | Produto: {produto} | Qtd: {qtd} | Pagamento: {forma} | Cliente: {cliente}")
        else:
            st.write("Nenhuma venda registrada.")
