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