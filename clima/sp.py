# dash.py
import requests
from conn.db_connection import Conexao
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
    


    def updates_cidades(self):
        geocodes = self.get_all_geocodes()

        previsoes = []
        ultimos_5_dias = ['manha', 'tarde', 'noite']

        if geocodes:
            hoje = datetime.now()
            datas = hoje.strftime('%d/%m/%Y')
            count = 0
            
            # Estabelecer conexão com o banco de dados
            cur = self.conn.cursor()

            for cidade_nome, geocode in geocodes:
                data = self.previsao(geocode)
                count += 1

                if data is None:
                    print(f"Nenhuma previsão encontrada para {cidade_nome} ({geocode}).")
                    continue

                previsao_dia = {'data': datas, 'cidade': cidade_nome, 'previsoes': {}}

                for periodo in ultimos_5_dias:
                    previsao_dia['previsoes'][periodo] = {
                        'uf': data[geocode][datas][periodo]['uf'],
                        'entidade': data[geocode][datas][periodo]['entidade'],
                        'resumo': data[geocode][datas][periodo]['resumo'],
                        'temp_max': data[geocode][datas][periodo]['temp_max'],
                        'temp_min': data[geocode][datas][periodo]['temp_min'],
                        'int_vento': data[geocode][datas][periodo]['int_vento'],
                        'umidade_max': data[geocode][datas][periodo]['umidade_max'],
                        'umidade_min': data[geocode][datas][periodo]['umidade_min'],
                        'temp_max_tende': data[geocode][datas][periodo]['temp_max_tende']
                    }

                    # Verificar se a previsão já existe no banco de dados
                    check_query = """
                        SELECT COUNT(*) FROM Leitura_Climatica
                        WHERE ID_Cidade = (SELECT ID_Cidade FROM Cidade WHERE Geocode = %s LIMIT 1)
                        AND periodo = %s;
                    """
                    cur.execute(check_query, (geocode, periodo))
                    exists = cur.fetchone()[0]

                    if exists == 0:
                        # Inserir no banco de dados se não existir
                        insert_query = """
                            INSERT INTO Leitura_Climatica (
                                uf, entidade, resumo, temp_max, temp_min, int_vento, 
                                umidade_max, umidade_min, temp_max_tende, periodo, ID_Cidade
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            (SELECT ID_Cidade FROM Cidade WHERE Geocode = %s LIMIT 1));
                        """
                        
                        valores = (
                            previsao_dia['previsoes'][periodo]['uf'],
                            previsao_dia['previsoes'][periodo]['entidade'],
                            previsao_dia['previsoes'][periodo]['resumo'],
                            previsao_dia['previsoes'][periodo]['temp_max'],
                            previsao_dia['previsoes'][periodo]['temp_min'],
                            previsao_dia['previsoes'][periodo]['int_vento'],
                            previsao_dia['previsoes'][periodo]['umidade_max'],
                            previsao_dia['previsoes'][periodo]['umidade_min'],
                            previsao_dia['previsoes'][periodo]['temp_max_tende'],
                            periodo,
                            geocode
                        )
                        
                        try:
                            cur.execute(insert_query, valores)
                            self.conn.commit()
                        except Exception as e:
                            print(f"Erro ao inserir previsão para {cidade_nome} ({geocode}) no período {periodo}: {e}")
                    else:
                        print(f"Previsão já existente para {cidade_nome} ({geocode}) no período {periodo}.")
                
                previsoes.append(previsao_dia)

            cur.close()
            return {'status': True, 'output': previsoes}
        else:
            return {'status': False, 'output': 'Nenhum geocode encontrado.'}

    def getCLimas(self):

        cur = self.conn.cursor()
        query = " SELECT * FROM Leitura_Climatica as leitura; "
        cur.execute(query)
        resultados = cur.fetchall()          
        for resultado in resultados:
            print(resultado)
            print(resultado[6])
            quit()

        

if __name__ == "__main__":
    sp = Sp()
    resultado = sp.getCLimas()