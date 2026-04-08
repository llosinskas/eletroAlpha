"""Classe para cálculo de correntes em circuitos monofásicos, bifásicos e trifásicos a partir da potência, tensão e fator de potência.
Autor: Lucas Losinskas
data: 04/2024
"""

import math

def Circuito_monofasico(demanda: float, tensao_fn: float, fator_potencia: float) -> float:
    """ Calcula a corrente de um circuito monofásico a partir da demanda, tensão fase-neutro e fator de potência.
    Args:
        demanda (float): Potência ativa da demanda da carga considerando equilibrada [W]
        tensao_fn (float): Tensão fase-neutro do circuito [V]
        fator_potencia (float): Fator de potência do circuito
    Returns:
        float: Corrente da carga [A]
    """
    corrente = demanda/(tensao_fn*fator_potencia)
    return corrente

def Circuito_bifasico(potencia: float, tensao_ff: float, fator_potencia: float) -> float:
    """ Cálcula a corrente de um circuito bifásico a partir da potência, tensão fase-fase e fator de potência.
    Args:
        potencia (float): Potência ativa da demanda da carga considerando equilibrada [W]
        tensao_ff (float): Tensão fase-fase do circuito [V]
        fator_potencia (float): Fator de potência do circuito
    Returns:
        float: Corrente da carga [A]
    """
    corrente = potencia/(tensao_ff*fator_potencia)
    return corrente

def Circuito_trifasico(potencia: float, tensao_ff: float, fator_potencia: float) -> float:
    """ Cálcula a corrente de um circuito trifásico a partir da potência, tensão fase-fase e fator de potência.
    Args:
        potencia (float): Potência ativa da demanda da carga considerando equilibrada [W]
        tensao_ff (float): Tensão fase-fase do circuito [V]
        fator_potencia (float): Fator de potência do circuito
    Returns:
        float: Corrente da carga [A]
    """
    corrente = potencia/(math.sqrt(3)*tensao_ff*fator_potencia)
    return corrente 

