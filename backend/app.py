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

#Variações de durações para tornar a rotina realista
duracoes_variaveis = [0.5, 1, 1.5, 2, 2.5]
duracoes_pesos = [10, 45, 20, 20, 5] #Probabilidades relativas para cada duração

#Função melhorada para gerar blocos de atividades com variação
def gerar_blocos_atividades(horas_totais, atividades_disponiveis, dia_semana):
    rotina_dia = []

    #Número de blocos varia com base no dia para quebrar a monotonia
    fatores_multiplicadores = {
        "Segunda" : 1,
        "Terça": 0.8,
        "Quarta": 1.2,
        "Quinta": 0.9,
        "Sexta": 1.1,
        "Sábado": 1.3,
        "Domingo": 0.7
    }

    #Multiplicador baseado no dia (variação de quantidade de blocos por dia)
    multiplicador = fatores_multiplicadores.get(dia_semana,1.0)
    horas_ajustadas = max(1, int(horas_totais * multiplicador))

    #Escolhe aleatoriamente quantos blocos serão criados (entre 1 e o número total de atividades disponíveis)
    num_blocos = min(len(atividades_disponiveis), random(1, horas_ajustadas))

    #Embaralha as atividades para maior variação e escolhe um subconjunto
    atividades_escolhidas = random.sample(atividades_disponiveis, num_blocos)

    #Distribui o tempo entre as atividades com variação
    for atividade in atividades_escolhidas:
        #Escolhe a duração com base nas probabilidades definidas anteriormente
        duracao = random.choices(duracoes_variaveis, weights=duracoes_pesos, k=1)[0]

        #Formata a duração
        duracao_formatada = f"{int(duracao)}h" if duracao.is_integer() else f"{duracao:.1f}h"

        rotina_dia.append(f"{duracao_formatada} de {atividade}")

    return rotina_dia


#Função para sugerir combinações de atividades complementares
def sugerir_combinacoes(atividade_principal, objetivo):
    combinacoes = {
        "Leitura": ["Cardio leve", "Alongamento", "Caminhada"],
        "Vídeo aula": ["Mobilidade", "Calistenia", "HIT"],
        "Musculação": ["Resumo", "Mapas mentais", "Audiolivros"],
        "Cardio": ["Flashcards", "Leitura leve", "Revisão"],
        "Yoga": ["Revisão", "Meditação", "Leitura reflexiva"],
        "Funcional": ["Leitura crítica", "Exercícios práticos", "Resumos"]
    }

    #Verifica se a atividade esta entre as principais
    for chave in combinacoes.keys():
        if chave.lower() in atividade_principal.lower():
            #Se o objetivo for "ambos", adiciona uma combinação
            if objetivo != "ambos" and random.random() < 0.3: #30% de chance
                complemento = random.choice(combinacoes[chave])
                return f"{atividade_principal} + {complemento}"
        
    return atividade_principal



#Função principal - gera rotina personalizada
def gerar_rotina_personalizada(objetivo, horas, time, dias):
    #Para cada dia, gera uma lista de atividade com tempo dividido
    rotina = {}

    for dia in dias:
        #Obtém a lista de atividades combase no objetivo e no turno
        atividades_turno = atividades_por_objetivo[objetivo][time]

        #Gera blocos variados para o dia
        blocos = gerar_blocos_atividades(horas, atividades_turno, dia)

        #Se não for "ambos", há chance de sugerir complementares
        if objetivo != "ambos":
            blocos_finais = []
            for bloco in blocos:
                partes = bloco.split(" de ", 1)
                if len(partes) == 2:
                    duracao, atividade = partes
                    atividade_final = sugerir_combinacoes(atividade, objetivo)
                    blocos_finais.append(f"{duracao} de {atividade_final}")
                else:
                    blocos_finais.append(bloco)
            blocos = blocos_finais

        #Atribui ao dia correspondente
        rotina[dia] = blocos

    return rotina

def adicionar_dicas_personalizadas(rotina, objetivo):
    dicas = {
        "estudo": [
            "Tenten alternar entre assuntos diferentes para manter o foco",
            "Faça pausas de 5 min a cada 25 min de estudo",
            "Revise seu material antes dormir para melhor assimilação",
            "Considere a técnica de estudo Feynman"
        ],
        "exercicio": [
            "Lembre-se de se hidratar adequadamente durante os exercícios",
            "Varie a intensidade/peso para evitar estagnação",
            "Faça alongamentos",
            "Use o fim de semana para recuperação ativa"
        ],
        "ambos": [
            "Equilibre atividades mentais e físicas para melhor rendimento",
            "Não se esqueça de incluir períodos de descanso na rotina",
            "Tente associar conceitos que você estudou durante atividades físicas leves",
            "Monitore seu progresso em ambas as áreas semanalmente"
        ]
    }

    #Escolhe de 1 a 2 dicas aleatorias 
    dicas_selecionadas = random.sample(dicas[objetivo], min(2,len(dicas[objetivo])))
    rotina["dicas"] = dicas_selecionadas

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

    #Adiciona dicas personalizadas
    rotina_com_dicas = adicionar_dicas_personalizadas(rotina, objetivo)

    return jsonify({
        "mensagem": f"{nome}, aqui está sua rotina personalizada!",
        "rotina": rotina_com_dicas
    })

#Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
