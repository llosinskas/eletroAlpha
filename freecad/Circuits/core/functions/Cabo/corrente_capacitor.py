def corrente_capacitor(corrente_nominal:float)->float:
    """Calcula a capacidade mínima do condutor para um capacitor a partir da corrente nominal do capacitor.
    Args:
        corrente_nominal (float): Corrente nominal do capacitor [A]
    Returns:
        float: Corrente mínima do condutor para o capacitor [A]
    """
    corrente = corrente_nominal*1.35
    return corrente