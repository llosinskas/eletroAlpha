def corrente_corrigida(corrente: float,fator_termico: float, fator_agrupamento: float) -> float:
    """Calcula a corrente corrigida a partir da corrente nominal e do fator de correção.
    Args:
        corrente (float): Corrente nominal do circuito [A]
        fator_termico (float): Fator de correção para temperatura
        fator_agrupamento (float): Fator de correção para agrupamento de condutores
    Returns:
        float: Corrente corrigida [A]
    """
    corrente_corrigida = corrente /(fator_termico*fator_agrupamento)
    return corrente_corrigida