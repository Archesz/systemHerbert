import streamlit as st
import json
import utils 
import graphs
import plotly.express as px
import operator
import pandas as pd
import plotly.graph_objects as go

from Database import Database
    
with open('simulados.json', 'r', encoding='utf-8') as json_file:
    simulados = json.load(json_file)

st.set_page_config(layout="wide", page_title="Analyzador",     
                    menu_items={
                        'Get Help': 'https://www.extremelycoolapp.com/help',
                        'Report a bug': "https://www.extremelycoolapp.com/bug",
                        'About': "# This is a header. This is an *extremely* cool app!",
                    })

def getPointsPeriod(students, periodo, simulado, materia):
    filtred = students.query(f"Periodo == '{periodo}'")

    all_points = []
    nomes = []
    for i in range(0, len(filtred)):
        try:
            gabarito = filtred.iloc[i]["Simulados"][simulado]["Gabarito"]
            id = filtred.iloc[i]["Primeiro Nome"]
            results = utils.compareResults(gabarito, simulados, simulado)

            if materia == "Geral":
                pontos = results[0]
            else:
                pontos = results[1][materia]

            all_points.append(int(pontos))
            nomes.append(id)

        except:
            pass

    df = pd.DataFrame({"Nome": nomes, "Pontos": all_points})
    df = df.sort_values(by="Pontos", ascending=False)

    return df


database = Database()

st.title("Análise dos Estudantes - Geral")

simulado = st.selectbox("Selecione o Simulado: ", list(simulados["Simulados"].keys()))
disciplinas = list(simulados["Simulados"][simulado]["Materias"])
disciplinas.insert(0, "Geral")

disciplina = st.selectbox("Disciplina: ", disciplinas)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Manhã")
    manha = getPointsPeriod(database.database, "Manhã", simulado, disciplina)
    manha

with col2:
    st.subheader("Tarde")
    tarde = getPointsPeriod(database.database, "Tarde", simulado, disciplina)
    tarde

with col3:
    st.subheader("Noturno")
    noite = getPointsPeriod(database.database, "Noite", simulado, disciplina)
    noite

fig = go.Figure()
fig.add_trace(go.Box(y=list(manha["Pontos"])))
fig.add_trace(go.Box(y=list(tarde["Pontos"])))
fig.add_trace(go.Box(y=list(noite["Pontos"])))
fig.update_layout(title_text="Distribuiçãod e Notas", labels={"trace 0": "Manhã", "trace 1": "Tarde", "trace 2": "Noite"})

st.plotly_chart(fig, use_container_width=True)
