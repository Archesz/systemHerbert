# Bibliotecas
import streamlit as st

# Páginas

# Classes
from Database import Database

#Configurações
st.set_page_config(layout="wide", page_title="Analyzador",     
                    menu_items={
                        'Get Help': 'https://www.extremelycoolapp.com/help',
                        'Report a bug': "https://www.extremelycoolapp.com/bug",
                        'About': "# This is a header. This is an *extremely* cool app!",
                    })

st.sidebar.title("Menu")

# Classes
database = Database()

# App

# student = database.find_student("HS2300015")
# st.write(student["Primeiro Nome"])