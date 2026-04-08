import unittest

from eletroAlpha.core.functions.queda_tensao import seccao_minima_queda_monofasica

class TestSecaoMinimaQuedaMonofasica(unittest.TestCase):
    
    def test_seccao_minima_queda_monofasica(self):
      
        # Teste 1: Potência de 1000 W, tensão de 127 V, fator de potência de 0.8, comprimento de 50 m e queda de tensão máxima de 5%

        correntes        = [7.9, 26.0, 28.8, 11.9, 28.8] # A
        comprimentos     = [8, 18, 24, 38, 49]           # m
        resistividade    = 1/56  # Ω.mm²/m (resistividade do cobre)
        tensao           = 380   # V    
        queda_max_tensao = 4     # %
        seccao_esperada  = 10    # mm² (valor aproximado)
        seccao_calculada = seccao_minima_queda_monofasica(correntes=correntes, comprimentos=comprimentos, resistividade=resistividade, tensao=tensao, queda_max_tensao=queda_max_tensao)
        self.assertAlmostEqual(seccao_calculada, seccao_esperada, delta=0.5)

unittest.main(verbosity=2)