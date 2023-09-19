import streamlit as st
import json
import utils 
import graphs
import plotly.express as px
import operator
import pandas as pd
import numpy as np
import random
import plotly.graph_objects as go

from Database import Database
    
with open('simulados.json', 'r', encoding='utf-8') as json_file:
    simulados = json.load(json_file)

# Gráficos
def calcularChance(total, corte):
    if total < corte:
        maximo = corte + 2
        chance = round((100 * total) / maximo, 2)
 
    elif total == corte:
        chance = 95
    
    elif total > corte + 2:
        chance = 100

    return chance

def acertosAluno(results, total):
    results["Total"] = total

    results = dict(sorted(results.items(), key=operator.itemgetter(1), reverse=True))

    fig = px.bar(x=list(results.keys()), y=list(results.values()), 
                 color=list(results.keys()),
                 title="Acertos por Disciplina", labels={"y": "Acertos", "x": "Disciplinas"})

    st.plotly_chart(fig, use_container_width=True)

def evolutionAluno(prova, id_select, materia):
    nome = prova.split("_")[0]
    nomes = simulados["Simulados"].keys()
    
    totais = []
    pontos = []
    names = []

    for prova in nomes:
        if nome in prova:
            total, acertos, deficts = database.desempenhoQuestoes(id_select, prova)
            totais.append(total)
            pontos.append(acertos)
            names.append(prova)

    if materia == "Geral":
        # Seus dados
        X = np.arange(0, len(names))
        Y = totais

        mean_x = np.mean(X)
        mean_y = np.mean(Y)

        numerator = 0
        denominator = 0

        for i in range(len(names)):  # Use len(names) em vez de 'n' para obter o comprimento correto
            numerator += (X[i] - mean_x) * (Y[i] - mean_y)
            denominator += (X[i] - mean_x) ** 2

        # Coeficiente angular (m)
        slope = numerator / denominator

        # Coeficiente linear (b)
        intercept = mean_y - slope * mean_x

        # Crie a linha de regressão
        regression_line = [slope * x + intercept for x in X]

        # Crie o gráfico Plotly
        fig = px.scatter(x=names, y=totais, 
                        title="Evolução", labels={"y": "Acertos", "x": "Provas"})

        # Adicione a linha de regressão
        fig.add_trace(go.Scatter(x=names, y=regression_line, mode='lines', name='Regressão Linear'))

        # Exiba o gráfico
        st.plotly_chart(fig, use_container_width=True)

    else:
        pontos_materia = []
        for i in pontos:
            pontos_materia.append(i[materia])

        fig = px.scatter(x=names, y=pontos_materia, 
                    title="Evolução", labels={"y": "Acertos", "x": "Provas"})

        st.plotly_chart(fig, use_container_width=True)

st.set_page_config(layout="wide", page_title="Analyzador",     
                    menu_items={
                        'Get Help': 'https://www.extremelycoolapp.com/help',
                        'Report a bug': "https://www.extremelycoolapp.com/bug",
                        'About': "# This is a header. This is an *extremely* cool app!",
                    })

database = Database()

st.title("Análise dos Estudantes")

simulado = st.selectbox("Selecione o Simulado: ", list(simulados["Simulados"].keys()))

students = list(database.database["Primeiro Nome"])[1::]
ids = list(database.database["id"])[1::]

student_select = st.selectbox("Selecione o Estudante", students)
id_select = ids[students.index(student_select)]

st.write(id_select, student_select)

student = database.find_student(id_select)

total, acertos, deficts = database.desempenhoQuestoes(id_select, simulado)

#st.write(acertos)

st.write(deficts)

acertosAluno(acertos, total)

disciplinas = list(simulados["Simulados"][simulado]["Materias"])
disciplinas.insert(0, "Geral")

disciplina = st.selectbox("Disciplina: ", disciplinas)

#evolutionAluno(simulado, id_select, disciplina)

def viewErros(id, simulado):
    erros = database.getErros(id, simulado)

    erros = dict(sorted(erros.items(), key=operator.itemgetter(1), reverse=True))

    fig = px.bar(x=list(erros.keys()), y=list(erros.values()), 
                 color=list(erros.keys()),
                 title="Erros por Temas", labels={"y": "Erros", "x": "Tema"})

    st.plotly_chart(fig, use_container_width=True)

viewErros(id_select, simulado)

st.divider()

st.subheader("Análise de Aprovação & Curso")

st.write("Selecione as Categorias que o Estudante se encaixa: ")

df = pd.read_csv("./bancas/Unicamp.csv", sep=",")
curso = st.selectbox("Selecione o Curso: ", list(df["Cursos"]))
ppi = st.checkbox("Preto, Parto ou Indigina?")
ep = st.selectbox("Escola Pública?", ["PAAIS 0", "PAAIS 20", "PAAIS 40", "PAAIS 60"])

if ppi:
    nota_corte = list(df.query(f"Cursos == '{curso}'")[f"C{ep}"])[0]
else:
    nota_corte = list(df.query(f"Cursos == '{curso}'")[ep])[0]

st.write(f"A Nota de Corte é: {nota_corte} Pontos. O aluno está com {total} Questões.")

chance = calcularChance(total, nota_corte)
st.write(f"Chance de Aprovação na Primeira Fase: {chance}%")


