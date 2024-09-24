# dash.py
import requests
from ..conn.db_connection import Conexao
from datetime import datetime, timedelta


class Sp:
    def __init__(self):
        conexao = Conexao(host="localhost", database="MetTechy", user="root", password="123")
        self.conn = conexao.conectar()    
    # def lista_cidades_sp(self):
    #     url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/35/municipios"
    #     response = requests.get(url)

    #     if response.status_code == 200:
    #         municipios = response.json()
    #         lista_cidades = [municipio['nome'] for municipio in municipios]
    #         return lista_cidades
    #     else:
    #         return []

    # def lista_geocode_sp(self):
    #     lista_cidades = self.lista_cidades_sp()  # Lista de cidades
    #     geocode_lista = []

    #     # Usando a classe de conexão
    #     conexao = Conexao(host="localhost", database="MetTechy", user="root", password="123")
    #     conn = conexao.conectar()
    #     if conn:
    #         cur = conn.cursor()

    #         for cidade in lista_cidades:
    #             url = f'https://apiprevmet3.inmet.gov.br/autocomplete/{cidade}'
    #             response = requests.get(url)

    #             if response.status_code == 200:
    #                 dados = response.json()

    #                 geoLoc = {
    #                     'nome': dados[0]['value'],
    #                     'uf': dados[0]['value'].split('-')[-1].strip(),
    #                     'geocode': dados[0]['geocode'],
    #                     'latitude': dados[0]['latitude'],
    #                     'longitude': dados[0]['longitude']
    #                 }

    #                 # Inserir no banco de dados
    #                 cur.execute(
    #                     """
    #                     INSERT INTO Cidade (Nome, Estado, Latitude, Longitude, Geocode)
    #                     VALUES (%s, %s, %s, %s, %s);
    #                     """,
            #             (geoLoc['nome'], geoLoc['uf'], geoLoc['latitude'], geoLoc['longitude'], geoLoc['geocode'])
            #         )
            #         print(f"Processando - {geoLoc}")
            #         conn.commit()

            #     else:
            #         print(f"Erro ao buscar dados para {cidade}: {response.status_code}")

            # # Confirme as transações e feche a conexão
            # cur.close()
            # conexao.desconectar()


    def previsao(self, geocode):
        url = f'https://apiprevmet3.inmet.gov.br/previsao/{geocode}'
        response = requests.get(url)
        
        if response.status_code == 200:
            dados = response.json()
            return dados
        else:
            print(f"Erro ao buscar previsão para geocode {geocode}: {response.status_code}")
            return {}  # Retorna um dicionário vazio em caso de erro

        
    def get_all_geocodes(self):
        try:
            cur = self.conn.cursor()
            # Consulta para pegar todos os geocodes e os nomes das cidades
            query = "SELECT Nome, Geocode FROM Cidade;"
            cur.execute(query)
            geocode_list = cur.fetchall()  # Pega todos os resultados
            cur.close()
            
            return geocode_list  # Retorna a lista de geocodes e nomes das cidades
        
        except Exception as e:
            print(f"Erro ao buscar geocodes no banco de dados: {e}")
            return []
    



    def previsao_para_todas_as_cidades(self):
        geocodes = self.get_all_geocodes()
        previsoes = []
        ultimos_5_dias = ['manha', 'tarde', 'noite']

        if geocodes:
            hoje = datetime.now()
            datas = (hoje).strftime('%d/%m/%Y') 
            print(datas)
            for cidade_nome, geocode in geocodes:
                data = self.previsao(geocode)

                if data is None:  # Verifica se data é None
                    print(f"Nenhuma previsão encontrada para {cidade_nome} ({geocode}).")
                    continue  # Pula para a próxima iteração

                for data_hoje in datas:
                    previsao_dia = {'data': data_hoje, 'cidade': cidade_nome, 'previsoes': {}}
        
                    for periodo in ultimos_5_dias:
                        if (geocode in data and 
                                data_hoje in data[geocode] and 
                                periodo in data[geocode][data_hoje]):
                                previsao_dia['previsoes'][periodo] = {
                                    'uf': data[geocode][data_hoje][periodo]['uf'],
                                    'entidade': data[geocode][data_hoje][periodo]['entidade'],
                                    'resumo': data[geocode][data_hoje][periodo]['resumo'],
                                    'temp_max': data[geocode][data_hoje][periodo]['temp_max'],
                                    'temp_min': data[geocode][data_hoje][periodo]['temp_min'],
                                    'int_vento': data[geocode][data_hoje][periodo]['int_vento'],
                                    'umidade_max': data[geocode][data_hoje][periodo]['umidade_max'],
                                    'umidade_min': data[geocode][data_hoje][periodo]['umidade_min'],
                                    'temp_max_tende': data[geocode][data_hoje][periodo]['temp_max_tende']
                            }
                                print(previsao_dia)
                    previsoes.append(previsao_dia)

                return {'status': True, 'output': previsoes}

