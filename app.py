from flask import Flask, render_template
from backend.clima.sp import Sp  # Ajuste a importação da sua classe conforme necessário

app = Flask(__name__)

@app.route('/')
def index():
    sp_instance = Sp()  # Cria uma instância da classe
    previsoes = sp_instance.previsao_para_todas_as_cidades()  # Chama o método para obter previsões
    print(previsoes)
    # Estrutura os dados para as previsões
    previsoes_estruturadas = []
    for previsao in previsoes['output']:
        cidade = previsao['cidade']
        data = previsao['data']
        
        # Extraindo informações de manhã, tarde e noite
        manha = previsao['previsoes'].get('manha', {})
        tarde = previsao['previsoes'].get('tarde', {})
        noite = previsao['previsoes'].get('noite', {})

        previsao_resumida = {
            'cidade': cidade,
            'data': data,
            'manha': {
                'resumo': manha.get('resumo', 'Não disponível'),
                'temp_max': manha.get('temp_max', 'Não disponível'),
                'temp_min': manha.get('temp_min', 'Não disponível')
            },
            'tarde': {
                'resumo': tarde.get('resumo', 'Não disponível'),
                'temp_max': tarde.get('temp_max', 'Não disponível'),
                'temp_min': tarde.get('temp_min', 'Não disponível')
            },
            'noite': {
                'resumo': noite.get('resumo', 'Não disponível'),
                'temp_max': noite.get('temp_max', 'Não disponível'),
                'temp_min': noite.get('temp_min', 'Não disponível')
            }
        }
        previsoes_estruturadas.append(previsao_resumida)

    return render_template('index.html', previsoes=previsoes_estruturadas)

if __name__ == '__main__':
    app.run(debug=True)
