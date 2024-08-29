# db_connection.py
import psycopg2
from psycopg2 import OperationalError

class Conexao:
    def __init__(self, host, database, user, password, port=5432):
        self.host = 'localhost'
        self.database = 'MetTechy'
        self.user = 'postgres'
        self.password = '123'
        self.port = '5432'
        self.conn = None

    def conectar(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("Conexão com o banco de dados estabelecida com sucesso.")
            return self.conn
        except OperationalError as e:
            print(f"Ocorreu um erro ao conectar ao banco de dados: {e}")
            return None

    def desconectar(self):
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados encerrada.")
