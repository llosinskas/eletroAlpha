# Dimensionamento de Barramentos 
# Autor Lucas Losinskas 
# Date: 2024
# E-mail: lucas_losinskas@hotmail.com

import math

class Barramento():
    
    def Sec_circular(diamentro_cabo):
        seccao_barramento = math.pi*(diamentro_cabo/2)**2
        return seccao_barramento
    
    def Sec_retangular(largura, altura):
        seccao_barramento = largura*altura
        return seccao_barramento
    
    def Sec_tubular(diametro_interno, diametro_externo):
        seccao_barramento = math.pi*(diametro_externo/2)**2-math.pi(diametro_interno/2)**2

# ====== Critérios para Dimensionar o Barramento =====
    # Capacidade de corrente do condutor em regime permanente
    # Retorna a Corrente de carga máxima [A]
    # Qc -> Quantidade de calor transferida para o meio ambiente por convecção [W/m]
    # Qr -> Quantidade de calor transferida para o meio ambiente por radiação [W/m]
    # Rc -> Resitência elétrica do material condutor [omega/m]
    def Corrente_carga_maxima(Qc, Qr, Qs, Rc):
        Ic = ((Qc*Qr-Qs)/Rc)**0.5
        return Ic

    # Capacidade de suportabilidade mecânica em razão das correntes de curto-circuito
    # Capacidade de suportabilidade térmica aos efeitos térmicos em função das correntes de curto-circuito
    # Dimensionamento sob o efeito corona. 
    # Critério da ressonância: vibração do condutor durante a condição de defeito
