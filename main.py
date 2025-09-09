import streamlit as st


st.title('Título')

st.text('Esta página apresenta o desenvolvimento de um pequeno sistema de controle de estoque voltado para uma cafeteria, simulando uma situação real de mercado. A proposta do projeto é criar uma ferramenta simples e funcional, que possa ser utilizada por pequenos comércios para gerenciar produtos e registrar vendas de forma prática e acessível.')

with st.sidebar:
    with st.sidebar:
        add_radio = st.radio(
        "Selecione as opções para escolher a página",
        ("Página 1","Página 2")
    )
        