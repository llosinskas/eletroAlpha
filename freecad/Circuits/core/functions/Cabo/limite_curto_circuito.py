import math

def seccao_minima_curto_circuito(Te: float, Ics:float, Tf:float, Ti:float)->float:
    """Calcula a seção mínima de um cabo para um curto-circuito a partir da temperatura de serviço contínuo, corrente de curto-circuito, temperatura limite de curto-circuito e temperatura inicial do condutor.
    Args:   
        Ics (float): Corrente de curto-circuito do circuito trifásica ou fase terra, a que for maior em [kA]
        Te (float): Tempo de eliminação de defeito [s]
        Tf (float): Temperatura máxima de curto-circuito suportado pela isolação do condutor[°C]
        Ti (float): Temperatura máxima adimissível pelo condutor em regime normal de operação [°C]
    Return: 
        float: Seção mínima do cabo [mm²] que suporte a corrente de curto-circuito por um tempo determinado pela temperatura limite de curto-circuito do material do condutor.
    """

    dividendo = math.sqrt(Te)*Ics
    divisor = 0.34*math.sqrt(math.log10((234+Tf)/(234+Ti)))

    seccao_minima = dividendo / divisor
    return seccao_minima

def limite_comprimento_circuito_curto_fase_terra(
        tensao_ff: float, 
        corrente_curto_circuito: float,
        imperdancia_seq_positiva_montante:float, 
        impedancia_seq_positiva_jusante:float,
    )-> float:
    """O comprimento de determinado circuito deve ser limitado em função da atuação do dispositivo de proteção contra curto circuito
    Args: 
        tensao_ff (float): Tensão fase-fase do circuito [V]
        corrente_curto_circuito (float): Corrente de curto-circuito do circuito trifásica ou fase terra, a que for maior em [kA]
        imperdancia_seq_positiva_montante (float): Impedância de sequência positiva do circuito montante ao ponto de instalação do dispositivo de proteção contra curto-circuito [Ω]
        impedancia_seq_positiva_jusante (float): Impedância de sequência positiva do circuito jusante ao ponto de instalação do dispositivo de proteção contra curto-circuito [Ω]
    Returns:
         float: Comprimento máximo do circuito para que o dispositivo de proteção contra curto-circuito atue corretamente.
    """
    comprimento = 0 
    potencia_cc = (0.95*tensao_ff)/(math.sqrt(3)*corrente_curto_circuito)  
    dividendo = potencia_cc - imperdancia_seq_positiva_montante
    divisor = 2*impedancia_seq_positiva_jusante/1000
    comprimento = dividendo/divisor
    return comprimento 
