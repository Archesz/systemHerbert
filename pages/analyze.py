# Bibliotecas
import streamlit as st
import json
import utils 
import graphs

# Classes
from Database import Database

with open('simulados.json', 'r', encoding='utf-8') as json_file:
    simulados = json.load(json_file)

st.set_page_config(layout="wide", page_title="Analyzador",     
                    menu_items={
                        'Get Help': 'https://www.extremelycoolapp.com/help',
                        'Report a bug': "https://www.extremelycoolapp.com/bug",
                        'About': "# This is a header. This is an *extremely* cool app!",
                    })

database = Database()

st.title("Análise dos Estudantes")

geral, especifico = st.tabs(["Geral", "Individual"])

simulado = st.selectbox("Selecione o Simulado: ", list(simulados["Simulados"].keys()))

st.divider()

with geral:
    st.write("Análise Geral")

    nomes, notas = graphs.viewAll(database, "Matemática", simulados, simulado)

    

with especifico:
    id_student = st.text_input("Digite o ID do Estudante:")

    if id_student != "Selecionar":
        student = database.find_student(id_student)

        total, acertos, deficts = utils.compareResults(student, simulados, simulado)
        medias = [7, 4, 3, 6, 4, 6, 4, 2, 3, 4]
        recomendados = [4, 6, 7, 2, 5, 8, 4, 7, 5, 2]

        graphs.desempenhoQuestoes(student, acertos, medias, recomendados)

        graphs.evolutionGraph(student, "Matemática")

        st.write(f"Total de Acertos: {total}")
        st.write(f"Total Médio: {sum(medias)}")
        st.write(f"Total Recomendado: {sum(recomendados)}")