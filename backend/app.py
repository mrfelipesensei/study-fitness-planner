from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app) # Libera requisções de outros domínios (como o frontend local)

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
