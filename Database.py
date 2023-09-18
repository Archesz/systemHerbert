import requests
import pandas as pd
import json

with open('simulados.json', 'r', encoding='utf-8') as json_file:
    simulados = json.load(json_file)

def compareResults(student, simulados, idProva):
    try:
      gabarito_student = student["Simulados"][idProva]["Gabarito"]
    except:
      gabarito_student = student

    gabarito_oficial = simulados["Simulados"][idProva]["Gabarito"]

    disciplinas_simulado = simulados["Simulados"][idProva]["Materias"]
    n_questoes = simulados["Simulados"][idProva]["Questao_Materia"]

    # Pegar total de acertos
    acertos_total = 0
    for i in range(0, len(gabarito_student)):
        if gabarito_student[i] == gabarito_oficial[i]:
            acertos_total += 1

    # Acertos por disciplina
    disciplinas_acertos = {}

    for disciplina in disciplinas_simulado:
        disciplinas_acertos[disciplina] = 0

    n_questao = 0
    questao = 1
    disciplina = disciplinas_simulado[n_questao]

    for i in range(0, len(gabarito_student)):
        if gabarito_student[i] == gabarito_oficial[i]:
            if questao > n_questoes[n_questao]:
                n_questao += 1
                disciplina = disciplinas_simulado[n_questao]

            disciplinas_acertos[disciplina] += 1

        questao += 1

    # Defict -> 1 - Erros / Total
    disciplinas_erros = {}

    keys = disciplinas_acertos.keys()

    for i, key in enumerate(keys):
      if i != 0:
        disciplinas_erros[key] = round(1 - (disciplinas_acertos[key] / (n_questoes[i] - n_questoes[i-1])), 2)
      else:
        disciplinas_erros[key] = round(1 - (disciplinas_acertos[key] / n_questoes[i]), 2)

    # Tags de erros -> Ver assuntos onde os alunos mais erraram

    return acertos_total, disciplinas_acertos, disciplinas_erros

class Database():
    def __init__(self):
      self.name = "Database Alunos"
      self.database_url = 'https://crudherbert-default-rtdb.firebaseio.com/'
      self.database, self.last_id = self.read_all()

    def find_student(self, id, name=None):
      node_path = f'usuarios/{id}'
      response = requests.get(f'{self.database_url}/{node_path}.json')

      if response.status_code == 200:
          data = response.json()
          return data

      else:
          print('Erro ao recuperar dados:', response.text)

    def find_name(self, name, get_id=True):
      query = self.database.query("`Primeiro Nome`.str.contains(@name, case=False, na=False)")
      if get_id == True:
        return list(query["id"])[0]
      else:
        return query

    def read_all(self):
        node_path = 'usuarios'
        response = requests.get(f'{self.database_url}/{node_path}.json')

        if response.status_code == 200:
            all_students_data = response.json()
            students_list = [{'id': key, **value}
                             for key, value in all_students_data.items()]
            df = pd.DataFrame(students_list)

            # Encontra o último ID
            last_id = max(all_students_data.keys())

            return df, last_id

    def insertNewStudent(self, cpf, nome, periodo):
        current_id = self.last_id
        new_id = self.increment_id(current_id)

        novo_aluno = {
            "Apelido": "",
            "Area": "",
            "CEP": "",
            "Celular": "",
            "Conquistas": [
                {
                    "Label": "Sou da primeira turma da plataforma!",
                    "Nome": "Pioneiro"
                }
            ],
            "Curso": "Vestibular",
            "Email": "",
            "ID": new_id,
            "Idade": "",
            "Nascimento": "",
            "Nivel": "Estudante",
            "Periodo": periodo,
            "Primeira Opção": "",
            "Primeiro Nome": nome,
            "RG": "",
            "Senha": cpf,
            "Simulados": {
            },
            "Sobrenome": "",
            "Social": {
                "Instagram": "",
                "Twitter": "",
                "Whatsapp": ""
            },
            "Status": "",
            "Turma": "",
            "URLFoto": "",
            "Universidade": ""
        }

        node_path = f'usuarios/{new_id}'
        response = requests.put(
            f'{self.database_url}/{node_path}.json', json=novo_aluno)

        if response.status_code == 200:
            print('Estudando Inserido com Sucesso!')
            self.last_id = new_id  # Atualiza o last_id após a inserção
        else:
            print('Erro ao inserir simulado:', response.text)

    def increment_id(self, current_id):
        prefix = current_id[:-7]
        number = int(current_id[-7:]) + 1
        new_id = f"{prefix}{number:07d}"
        return new_id

    def insertSimulado(self, id, nome, respostas):
        novo_simulado = {
            'Gabarito': respostas
        }

        node_path = f'usuarios/{id}/Simulados/{nome}'
        response = requests.put(f'{self.database_url}/{node_path}.json', json=novo_simulado)

        if response.status_code == 200:
            print('Simulado inserido com sucesso!')
        else:
            print('Erro ao inserir simulado:', response.text)

    def readStudent(self, id):
        node_path = f'usuarios/{id}'
        response = requests.get(f'{self.database_url}/{node_path}.json')

        if response.status_code == 200:
            data = response.json()
            return data

        else:
            print('Erro ao recuperar dados:', response.text)

    def desempenhoQuestoes(self, ID, prova):
        student = self.readStudent(ID)
        total, acertos, deficts = compareResults(student, simulados, prova)
        return total, acertos, deficts
    
    def getErros(self, ID, prova):
        student = self.readStudent(ID)
        erros = {}

        try:
            gabarito_student = student["Simulados"][prova]["Gabarito"]
        except:
            gabarito_student = student

        gabarito_oficial = simulados["Simulados"][prova]["Gabarito"]

        for i in range(0, len(gabarito_student)):
            if gabarito_student[i] != gabarito_oficial[i]:
                tags = simulados["Simulados"][prova]["Tags"][i]
                for tag in tags:
                    if tag not in erros:
                      erros[tag] = 1
                    else:
                       erros[tag] += 1

        return erros