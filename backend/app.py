from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import math

app = Flask(__name__)
CORS(app) # Libera requisções de outros domínios (como o frontend local)

#Atividades organizadas por objetivo e turno do dia
atividades_por_objetivo = {
    "estudo": {
        "manha": ["Leitura", "Vídeo aula", "Exercícios práticos", "Resumos"],
        "tarde": ["Vídeo aula", "Leitura crítica", "Mapas mentais", "Flashcards"],
        "noite": ["Revisão", "Leitura leve", "Simulados", "Organização de anotações"]
    },
    "exercicio": {
        "manha": ["Musculação", "Cardio HIT", "Alongamento"],
        "tarde": ["Funcional", "Cardio leve", "Mobilidade"],
        "noite": ["Yoga", "Alongamento relaxante", "Caminhada"]
    },
    "ambos": {
        "manha": ["Leitura + Cardio", "Musculação + Resumo", "Mobilidade + Vídeo aula"],
        "tarde": ["Cardio + Video aula", "Funcional + Leitura crítica","Cardio HIT + Flashcards"],
        "noite": ["Yoga + Revisão", "Alongamento + Resumo", "Cardio leve + Mapas mentais"]
    }
}

#Função para dividir as horas/blocos de atividades
def dividir_horas_em_blocos(horas_totais, atividades_disponiveis):

    num_blocos = min(len(atividades_disponiveis), horas_totais)
    horas_por_bloco = horas_totais // num_blocos #arredonda para baixo

    atividades_escolhidas = random.sample(atividades_disponiveis, num_blocos)
    rotina_dia = []

    for atividade in atividades_disponiveis:
        rotina_dia.append(f"{horas_por_bloco}h de {atividade}")

    return rotina_dia

#Função principal - gera rotina personalizada
def gerar_rotina_personalizada(objetivo, horas, time, dias):
    #Para cada dia, gera uma lista de atividade com tempo dividido
    rotina = {}

    for dia in dias:
        #Obtém a lista de atividades com base no objetivo e no turno
        atividades_turno = atividades_por_objetivo[objetivo][time]

        #Divide o tempo entre as atividades
        blocos = dividir_horas_em_blocos(horas, atividades_turno)

        #Atribui ao dia correspondente
        rotina[dia] = blocos

    return rotina



@app.route('/gerar-rotina', methods=['POST'])
def gerar_rotina():
    dados = request.json
    objetivo = dados.get("goal")
    horas = dados.get("hours")
    time = dados.get("time")
    dias = dados.get("days")

    atividades = {
        "estudo" : ["Leitura", "Vídeo aula", "Exercícios práticos", "Revisão"],
        "exercicio" : ["Musculação", "Cardio", "Alongamento", "Funcional"],
        "ambos" : ["Estudo + Musculação", "Cardio + Leitura", "Revisão + Treino"]
    }

    rotina = {}
    for dia in dias:
        if objetivo == "ambos":
            atividade = random.choice(atividades["ambos"])
        else:
            atividade = f"{random.choice(atividades[objetivo])} por {horas}h na {time}"
        rotina[dia] = atividade

    return jsonify(rotina)


if __name__ == '__main__':
    app.run(debug=True)
