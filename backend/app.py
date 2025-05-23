from flask import Flask, request, jsonify
from flask_cors import CORS
import random


app = Flask(__name__)
CORS(app) # Libera requisções de outros domínios (como o frontend local)

#Atividades organizadas por objetivo e turno do dia
#Adicionando mais variedades de atividades
atividades_por_objetivo = {
    "estudo": {
        "manha": ["Leitura", "Vídeo aula", "Exercícios práticos", "Resumos", "Estudo em grupo",
                  "Revisão de anotações", "Preparação de materiais", "Pesquisa acadêmica"],
        "tarde": ["Vídeo aula", "Leitura crítica", "Mapas mentais", "Flashcards" "Prática de problemas",
                  "Estudos de caso", "Aulas online", "Leitura de artigos"],
        "noite": ["Revisão", "Leitura leve", "Simulados", "Organização de anotações", "Estudo focado",
                  "Aúdio livros", "Resumo do dia", "Planejamento do dia seguinte"]
    },
    "exercicio": {
        "manha": ["Musculação", "Cardio HIT", "Alongamento", "Corrida", "Caminhada", "Elíptico", 
                  "Pilates", "Treino funcional"],
        "tarde": ["Funcional", "Cardio leve", "Mobilidade", "Peso livre", "Treino de força",
                  "Calistenia", "Treino intervalado"],
        "noite": ["Yoga", "Alongamento relaxante", "Caminhada", "Dança", "Mobilidade",
                  "Corrida"]
    },
    "ambos": {
        "manha": ["Leitura + Cardio", "Musculação + Resumo", "Mobilidade + Vídeo aula", 
                  "Corrida + Flashcards", "Caminhada + Mapas mentais", "Funcional + Revisão"],
        "tarde": ["Cardio + Video aula", "Funcional + Leitura crítica","Cardio HIT + Flashcards",
                  "Treino de força + Pesquisa", "Corrida + Leitura", "Calistenia + Estudos de caso"],
        "noite": ["Yoga + Revisão", "Alongamento + Resumo", "Cardio leve + Mapas mentais",
                  "Meditação + Leitura", "Dança + Organização", "Pilates + Áudio livros"]
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


#Rota da API que responde à requisição do frontend
@app.route('/gerar-rotina', methods=['POST'])
def gerar_rotina():
    dados = request.json

    nome = dados.get("name", "Usuário") #Se não enviar name, enviará "Usuário"
    objetivo = dados.get("goal")
    horas = int(dados.get("hours",1))
    time = dados.get("time")
    dias = dados.get("days", [])

    #Gera a rotina baseada nas preferências
    rotina = gerar_rotina_personalizada(objetivo, horas, time, dias)

    return jsonify({
        "mensagem": f"{nome}, aqui está sua rotina personalizada!",
        "rotina": rotina
    })

#Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
