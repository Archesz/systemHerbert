# Bibliotecas
import streamlit as st

# Classes
from Database import Database

st.set_page_config(layout="wide", page_title="Analyzador",     
                    menu_items={
                        'Get Help': 'https://www.extremelycoolapp.com/help',
                        'Report a bug': "https://www.extremelycoolapp.com/bug",
                        'About': "# This is a header. This is an *extremely* cool app!",
                    })

database = Database()
dataframe, _ = database.read_all()

st.title("Banco de Dados")
    
read, create, analyse = st.tabs(["Leitura", "Cadastro", "Analisar"])

with read:
    
    # Inputs para filtro
    col1, col2, col3 = st.columns(3)

    nome_input = st.text_input("Nome")

    with col1:
        id_input = st.text_input("ID")
    
    with col2:
        periodo_input = st.selectbox("Periodo", ["Geral", "Manhã", "Tarde", "Noite"])
    
    with col3:
        cpf_input = st.text_input("CPF")
    
    filtro = st.button("Filtrar")
    # Aplica os filtros se os inputs estiverem preenchidos

    if filtro:
        if nome_input:
            dataframe = dataframe[dataframe["Primeiro Nome"].str.contains(nome_input, case=False)]

        if id_input:
            dataframe = dataframe[dataframe["id"].str.contains(id_input, case=False)]

        if periodo_input != "Geral":
            dataframe = dataframe[dataframe["Periodo"].str.contains(periodo_input, case=False)]
            
        if cpf_input:
            dataframe = dataframe[dataframe["Senha"].str.contains(cpf_input, case=False)]

    # Mostra o DataFrame filtrado
    st.dataframe(dataframe)

with create:
    col1, col2, col3 = st.columns(3)

    nome_new = st.text_input("Nome do Estudante")
    
    with col1:
        cpf_new = st.text_input("CPF do Estudante")
    
    with col2:
        periodo_new = st.selectbox("Período", ["Manhã", "Tarde", "Noite"])

    cadastrar = st.button("Cadastrar")

    if cadastrar:
        database.insertNewStudent(cpf_new, nome_new, periodo_new)

        st.success("Estudante Cadastrado com Sucesso!")