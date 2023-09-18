import streamlit as st
import json
from Database import Database

def processGabarito(gabarito):
    gabarito = gabarito.upper()
    gabarito = list(gabarito)
    return gabarito

with open('simulados.json', 'r', encoding='utf-8') as json_file:
    simulados = json.load(json_file)

database = Database()
dataframe, _ = database.read_all()

simulado_select = st.selectbox("Selecione o Simulado: ", list(simulados["Simulados"].keys()))
simulado = simulados["Simulados"][simulado_select]

students = list(dataframe["Primeiro Nome"])
ids = list(dataframe["id"])

student_select = st.selectbox("Selecione o Estudante", students)
id_select = ids[students.index(student_select)]

st.write(id_select, student_select)

gabarito_aluno = st.text_input("")

gabarito_processado = processGabarito(gabarito_aluno)
st.write(gabarito_processado)

btn = st.button("Enviar")

if btn:
    try:
        database.insertSimulado(id_select, simulado_select, gabarito_processado)
        st.success("Simulado Cadastrado")
    except:
        st.error("Falha ao inserir.")
        
#simulado