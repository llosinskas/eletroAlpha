import math 

def seccao_minima_queda_monofasica(correntes: list[float], comprimentos:list[float], resistividade:float, tensao:float, queda_max_tensao:float) -> float:
    """Calcula a seção mínima de um cabo para um circuito monofásico a partir da corrente, comprimento do circuito e fator de potência.
    Args:
        correntes (list[float]): Lista de correntes da carga [A]
        comprimentos (list[float]): Lista de comprimentos dos circuitos [m]
        resistividade (float): Resistividade do material do condutor [Ω.mm²/m]    
        tensao (float): Tensão nominal do circuito monofásico fase-neutro ou bifásico fase-fase [V]
        queda_max_tensao (float): Queda máxima de tensão permitida [%]
    returns:
        float: Seção mínima do cabo [mm²]
    """
    soma = 0
    for i, comprimento in enumerate(comprimentos):
        soma += comprimento*correntes[i]

    dividendo = 200*resistividade*soma
    divisor = tensao*queda_max_tensao
    seccao_minima = dividendo/divisor
    return seccao_minima 
    
def seccao_minima_queda_trifasica(correntes: list[float], comprimentos:list[float], resistividade:float, tensao:float, queda_max_tensao:float) -> float:
    """ Calcula a seção mínima de um cabo para um circuito trifásico a partir da corrente, comprimento do circuito e fator de potência.
    Args: 
        correntes (list[float]): Lista de correntes da carga [A]
        comprimentos (list[float]): Lista de comprimentos dos circuitos [m]
        resistividade (float): Resistividade do material do condutor [Ω.mm²/m]    
        tensao (float): Tensão nominal do circuito trifásico fase-fase [V]
        queda_max_tensao (float): Queda máxima de tensão permitida [%]
     Returns:
         float: Seção mínima do cabo [mm²] """
    soma=0
    for i, comprimento in enumerate(comprimentos):
        soma += comprimento*correntes[i]
    dividendo = 100*math.sqrt(3)*resistividade*soma
    divisor = tensao*queda_max_tensao
    seccao_minima = dividendo/divisor
    return seccao_minima

def queda_tensao_trifasico(corrente: float, resistencia_condutor: float, reatancia_condutor:float, comprimento:float, fator_potencia:float, tensao_ff: float, N_cp: int)->float:
    """Calcula a queda de tensão em um circuito trifásico a partir da corrente, comprimento do circuito e fator de potência.
    Args:
        corrente (float): Corrente da carga [A]
        resistencia_condutor (float): Resistência do condutor [mΩ/km]
        reatancia_condutor (float): Reatância do condutor [mΩ/km]
        comprimento (float): Comprimento do circuito [m]
        fator_potencia (float): Fator de potência do circuito
        tensao_ff (float): Tensão fase-fase do circuito [V]
        N_cp (int): Número de condutores em paralelopor fase
    Returns:
        float: Queda de tensão no circuito [%]
    """
    angulo = math.acos(fator_potencia)
    resistencia_circuito = resistencia_condutor*math.cos(angulo)
    reatancia_circuito = reatancia_condutor*math.sin(angulo)
    
    dividendo = math.sqrt(3)*corrente*comprimento(resistencia_circuito+reatancia_circuito)
    divisor = 10*tensao_ff*N_cp 
    queda_tensao = dividendo/divisor

    return queda_tensao 