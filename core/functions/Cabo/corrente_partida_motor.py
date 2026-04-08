def corrente_motor(corrente_nominal:float, fator_servico:float)->float:
    """Calcula a corrente de um motor a partir da corrente nominal e do fator de serviço.
    Args:
        corrente_nominal (float): Corrente nominal do motor [A]
        fator_servico (float): Fator de serviço do motor
    Returns:
        float: Corrente do motor considerando o fator de serviço [A]
    """
    corrente = corrente_nominal*fator_servico
    return corrente

def corrente_grupo_motores(correntes_nominais: list[float], fator_servico:list[float])->float:
    """Calcula a corrente de um grupo de motores a partir das correntes nominais e do fator de serviço.
    Args:
        correntes_nominais (list[float]): Lista de correntes nominais dos motores [A]
        fator_servico (list[float]): Lista de fatores de serviço dos motores
    Returns:
        float: Corrente do grupo de motores considerando o fator de serviço [A]
    """
    corrente_partirda = 0
    for i, corrente in enumerate(correntes_nominais):
        corrente_partirda += corrente*fator_servico[i]
    return corrente_partirda