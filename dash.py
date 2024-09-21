# dash.py
import requests
from clima.sp import Sp

class dash:
    
    def __init__(self):
        clima = Sp()  
        self.previsaoSp = clima.previsao_para_todas_as_cidades() 
        

    def service_sp(self):
        print(self.previsaoSp)


if __name__ == "__main__":
    clima = dash()
    clima.service_sp()
