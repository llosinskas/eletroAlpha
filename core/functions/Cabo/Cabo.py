# Autor: Lucas Losinskas
# data: 04/2024
# Classe para o dimensionamento de cabos segundo a NBR 5410/2004 

from enum import Enum


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

