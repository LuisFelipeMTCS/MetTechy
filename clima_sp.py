# dash.py
import requests
from db_connection import Conexao

class ClimaSp:
    
    def lista_cidades_sp(self):
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/35/municipios"
        response = requests.get(url)

        if response.status_code == 200:
            municipios = response.json()
            lista_cidades = [municipio['nome'] for municipio in municipios]
            return lista_cidades
        else:
            return []

    def lista_geocode_sp(self):
        lista_cidades = self.lista_cidades_sp()  # Lista de cidades
        geocode_lista = []

        # Usando a classe de conexão
        conexao = Conexao(host="localhost", database="MetTechy", user="root", password="123")
        conn = conexao.conectar()
        if conn:
            cur = conn.cursor()

            for cidade in lista_cidades:
                url = f'https://apiprevmet3.inmet.gov.br/autocomplete/{cidade}'
                response = requests.get(url)

                if response.status_code == 200:
                    dados = response.json()

                    geoLoc = {
                        'nome': dados[0]['value'],
                        'uf': dados[0]['value'].split('-')[-1].strip(),
                        'geocode': dados[0]['geocode'],
                        'latitude': dados[0]['latitude'],
                        'longitude': dados[0]['longitude']
                    }

                    # Inserir no banco de dados
                    cur.execute(
                        """
                        INSERT INTO Cidade (Nome, Estado, Latitude, Longitude, Geocode)
                        VALUES (%s, %s, %s, %s, %s);
                        """,
                        (geoLoc['nome'], geoLoc['uf'], geoLoc['latitude'], geoLoc['longitude'], geoLoc['geocode'])
                    )
                    print(f"Processando - {geoLoc}")
                    conn.commit()

                else:
                    print(f"Erro ao buscar dados para {cidade}: {response.status_code}")

            # Confirme as transações e feche a conexão
            cur.close()
            conexao.desconectar()

    

# Exemplo de uso
clima = ClimaSp()
print(clima.lista_geocode_sp())  # Lista de geocodes
