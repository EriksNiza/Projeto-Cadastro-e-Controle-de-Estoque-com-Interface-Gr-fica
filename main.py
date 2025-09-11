import streamlit as st

with st.sidebar:
    st.title('Menu')
    pagina = st.selectbox(
        'Selecione uma das páginas',
        ['Cadastro de produtos', 'Registro de vendas']
    )

if pagina == 'Cadastro de produtos':
    st.header("Cadastro de Produtos")

    with st.expander('Registre seus produtos'):
        nome_prod = st.text_input('Insira no nome do produto: ')
        preco_prod = st.number_input('Insira o preço do produto: ')
        estoque_prod = st.slider('Insira a quantidade em estoque: ', 0, 200)
        enviar_prod = st.button('Enviar')

        if enviar_prod:
            st.success(f"Produto '{nome_prod}' cadastrado com sucesso!")
        
    with st.expander('Visualize seus produtos'):
        st.title('Oi')

elif pagina == 'Registro de vendas':

    st.header("Registro de Vendas")
    st.expander('')
