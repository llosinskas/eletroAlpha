# Autor: Lucas Losinskas
# data: 04/2024
# Classe para o dimensionamento de cabos segundo a NBR 5410/2004 

from enum import Enum
import math 

class Metodos(Enum):
        A1  = 0 # Condutores isolados em eletrodutos de seção circular embuitdo em parede termicamente isolante
        A2  = 1 # Cabo unipolar em eletroduto de seção circular embutido em parede termicamente isolante
        B1  = 2 # Condutores isolados em eletroduto de seção circular sobre a parede de madeira 
        B2  = 3 # Cabo multipolar em eletroduto de seção circular sobre parede de madeira 
        C   = 4 # Cabos unipolares ou cabo multipolar enterrados no solo
        D   = 5 # Cabo multipolar em eletroduto enterrado no solo
        E   = 6 # Cabo multipolar ao ar livre
        F   = 7 # Cabos unipolares (na horizontal, vertical ou em trifólio) ao ar livre
        G   = 8 # Cabos unipolares espaçados ao ar livre 

class Material(Enum):
    PVC     = 0 # Cloreto de povinila
    EPR     = 1 # Borracha etileno-propileno
    XLPE    = 2 # Polietileno reticulado 
    
    # Retorna a temperatura máxima para serviço contínuo do condutor [°C] 
    @classmethod
    def temp_servico_continuo(material) -> float:
        if material == 0:
            temp = 70
        elif material ==1: 
            temp = 90
        elif material == 2:
            temp = 90
        return temp 
    
    # Retorna a temperatura limite de sobre carga do condutor [°C]
    @classmethod
    def temp_sobrecarga(material) -> float:
        if material == 0:
            temp = 100
        elif material ==1: 
            temp = 130
        elif material == 2:
            temp = 130
        return temp 

    # Retorna a temperatura limite de curto-circuto do condutor [°C]
    @classmethod
    def temp_sobrecarga(material) -> float:
        if material == 0:
            temp = 160
        elif material ==1: 
            temp = 250
        elif material == 2:
            temp = 250
        return temp 

# Critério da capacidade de condução de corrente 
# Retorna a corrente da carga [A]
# tensao_fn: tensao fase neutro do circuito [V]
# fator_potencia: Fator de potencia do circuito 
def Circuito_monofasico(demanda, tensao_fn, fator_potencia) -> float:
    corrente = demanda/(tensao_fn*fator_potencia)
    return corrente

# Retorna a corrente da carga [A]
# potencia: Potência ativa da demanda da carga considerando equilibrada [W]
# tensao_ff: tensão fase fase [V]
def Circuito_trifasico(potencia, tensao_ff, fator_potencia) -> float:
    corrente = potencia/(math.sqrt(3)*tensao_ff*fator_potencia)
    return corrente 




def seccao():
    tabela_PVC = [  
        (7,7,7,7,9,8,9,8,10,9,12,10),                               # 0.5mm² 
        (9,9,9,9,11,10,11,10,13,11,15,12),                          # 0.75mm²
        (11,10,11,10,14,12,13,12,15,14,18,15),                      # 1mm²
        (14.5, 13.5, 14, 13,17.5,15.5,16.5,15,19.5,17.5,22,18),     # 1.5mm²
        (19.5,18,18.5,17.5,24,21,23,20,27,24,29,24),                # 2.5mm²
        ()
    ]
    tabela_EPR = [
        
    ]