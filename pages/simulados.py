# Página para Realizar o processamento do Simulado

# Bibliotecas
import streamlit as st
import json
import utils 
import graphs
import requests

# Funções
def processarSimulado(database, simulado):
    students, _ = database.read_all()
    ids = list(students["id"])
    database_url = 'https://crudherbert-default-rtdb.firebaseio.com/'

    for id in ids:
        student = database.find_student(id)
        try:
            total, acertos, deficts = utils.compareResults(student, simulados, simulado)
            node_path = student["id"]
            print(node_path)
            response = requests.put(f'{database_url}/usuarios/{node_path}/Simulados/{simulado}/desempenho.json', json=acertos)
            print("ok")
        except:
            continue


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

st.title("Gerenciamento de Simulados")

st.header("Processar Simulados")
st.write("Ao processar o simulado, as notas dos alunos irão ser anexadas em cada estudante.")

simulado = st.selectbox("Selecione o Simulado", simulados["Simulados"].keys())

btn_proccess = st.button("Processar Simulado")

if btn_proccess:
    processarSimulado(database, simulado)