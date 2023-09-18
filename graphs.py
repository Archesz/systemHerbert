import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import utils

def desempenhoQuestoes(student, acertos, medias, recomendados):
    y = list(acertos.values())
    x = list(acertos.keys())
    fig = px.bar(title=f"Análise de Desempenho ({student['Primeiro Nome']})",
                 labels={"x": "Disciplinas", "y": "Acertos"}, 
                 barmode='group')
    
    fig.add_bar(x=x, y=y, name="Acertos")
    fig.add_bar(x=x, y=medias, name="Médias")
    fig.add_bar(x=x, y=recomendados, name="Recomendados")

    st.plotly_chart(fig, use_container_width=True)

def evolutionGraph(student, disciplina):
    x = ["Unicamp_0001", "Fuvest_0001", "Unicamp_0002", "Fuvest_0002", "Unicamp_0003", "Fuvest_0003", "Unicamp_0004", "Fuvest_0004"]
    y = [0.94, 0.86, 0.80, 0.74, 0.58, 0.64, 0.48, 0.39]
    acertos = [1, 3, 4, 6, 8, 7, 9, 11]

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=x, y=y, name="Défict"))
    fig.update_layout(title="Défict")

    st.plotly_chart(fig, use_container_width=True)

    fig_2 = go.Figure()
    fig_2.add_trace(go.Scatter(x=x, y=acertos, mode='lines+markers', name="Acertos"))

    slope, intercept = np.polyfit(range(len(acertos)), acertos, 1)
    line = slope * np.array(range(len(acertos))) + intercept

    num_extra_points = 2  # Número de pontos previstos
    x_extra = x + [f"Future_{i}" for i in range(num_extra_points)]
    y_extra = list(line) + [line[-1] + slope * i for i in range(1, num_extra_points + 1)]

    fig_2.add_trace(go.Scatter(x=x_extra, y=y_extra, mode='lines', name="Regressão Linear Estendida"))
    fig_2.update_layout(title="Acertos de Questões")

    st.plotly_chart(fig_2, use_container_width=True)

def viewAll(database, materia, simulados, simulado):
    students, _ = database.read_all()
    ids = list(students["id"])

    nomes = []
    notas = []

    for id in ids:
        student = database.find_student(id)
        try:
            total, acertos, deficts = utils.compareResults(student, simulados, simulado)
            nomes.append(student["Primeiro Nome"])
            notas.append(acertos[materia])

        except:
            continue
    
    return nomes, notas
